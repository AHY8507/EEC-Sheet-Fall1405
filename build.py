#!/usr/bin/env python3
"""Build the study-notes site.

    python3 build.py                 -> docs/index.html  (GitHub Pages, full HTML document)
    python3 build.py --artifact OUT  -> OUT              (same page without <html>/<head>/<body>, for a claude.ai Artifact)

Sources:
    src/chapters/<route>.html   chapter bodies written with a few shorthand tags (see expand())
    src/circuits/*.py           schemdraw circuits registered with @ckt('name')
    src/style.css, src/app.js   inlined into the page
"""
import html
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / 'src'
sys.path.insert(0, str(SRC))
import ck  # noqa: E402

FA = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def fa(x):
    return str(x).translate(FA)


# ----------------------------------------------------------------------------------------------
# Manifest: parts and chapters.  (route, code, title, one-line description, syllabus coverage)
# ----------------------------------------------------------------------------------------------
PARTS = [
    ('A', 'پایه‌ها: ریاضی و فیزیکِ لازم', 'هر چیزی که درس مدار روی آن سوار است، از صفر', [
        ('math-functions', 'A1', 'تابع، شیب، نمایی و لگاریتم', 'زبان نمودارها؛ چرا عدد e همه‌جای مدار پیدا می‌شود', 'پیش‌نیاز همه فصل‌ها'),
        ('math-trig-complex', 'A2', 'سینوسی‌ها و اعداد مختلط', 'دامنه، فرکانس، فاز؛ بردار چرخان و فرمول اویلر', 'پیش‌نیاز مرتبه دوم و لاپلاس'),
        ('math-derivative', 'A3', 'مشتق: آهنگ تغییر', 'از شیب وتر تا مشتق؛ همه قاعده‌ها با اثبات', 'پیش‌نیاز خازن و سلف'),
        ('math-integral', 'A4', 'انتگرال، پله و ضربه', 'جمع تکه‌های کوچک؛ مساحت؛ قضیه اساسی؛ u(t) و δ(t)', 'پیش‌نیاز خازن و سلف'),
        ('math-linear', 'A5', 'دستگاه معادلات خطی', 'حذف، جایگذاری، کرامر و نوشتن ماتریسی', 'پیش‌نیاز تحلیل گره و مش'),
        ('math-ode', 'A6', 'معادلات دیفرانسیل مدار', 'مرتبه اول و دوم؛ معادله مشخصه؛ جواب همگن و خصوصی', 'پیش‌نیاز مدارهای مرتبه اول و دوم'),
        ('phys-electric', 'A7', 'فیزیک الکتریسیته', 'بار، میدان، ولتاژ، جریان، مقاومت و خازن فیزیکی', 'پیش‌نیاز فصل ۱ و ۲ درس'),
        ('phys-magnetic', 'A8', 'مغناطیس و القا', 'شار، قانون فارادی، لنز و سلف فیزیکی', 'پیش‌نیاز سلف'),
    ]),
    ('B', 'مدارهای الکتریکی', 'فصل‌های ۱ تا ۳ درس · پوشش میان‌ترم', [
        ('elements', 'B1', 'المان‌ها و منابع', 'کمیت‌های پایه، مقاومت، خطی بودن، منابع مستقل و وابسته', 'فصل ۱ درس · کوییز I · میان‌ترم'),
        ('kirchhoff', 'B2', 'قوانین کیرشهف و ترکیب مقاومت‌ها', 'KCL، KVL، سری و موازی، تقسیم ولتاژ و جریان، تبدیل منبع، ستاره-مثلث', 'فصل ۱ درس · کوییز I · میان‌ترم'),
        ('nodal-mesh', 'B3', 'تحلیل گره و مش', 'ابرگره، ابرمش، منابع وابسته و روش بازرسی', 'فصل ۱ درس · کوییز I · میان‌ترم'),
        ('thevenin', 'B4', 'خطی بودن، جمع آثار، تونن و نورتن', 'همگنی، برهم‌نهی، مدار معادل و انتقال حداکثر توان', 'فصل ۱ درس · کوییز I و II · میان‌ترم'),
        ('opamp', 'B5', 'تقویت‌کننده عملیاتی', 'مدل ایده‌آل، اتصال کوتاه مجازی، معکوس‌کننده، جمع‌کننده، تفاضلی', 'از جزوه کلاس'),
        ('capacitor', 'B6', 'خازن', 'رابطه جریان و ولتاژ، پیوستگی ولتاژ، انرژی، سری و موازی، اتصال خازن‌های باردار', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('inductor', 'B7', 'سلف و دوگانی', 'رابطه ولتاژ و جریان، پیوستگی جریان، انرژی، ترکیب سلف‌ها، مدار دوگان', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('waveforms', 'B8', 'شکل موج‌ها', 'پله، شیب، ضربه، پالس، نمایی و سینوسی؛ ساختن موج از قطعه‌ها', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('switching', 'B9', 'حالت دائمی DC و لحظه کلیدزنی', 'مقادیر 0⁻ و 0⁺ و ∞ و مشتق‌های اولیه', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('order', 'B10', 'مرتبه مدار', 'حلقه خازنی، کات‌ست سلفی و روش سریع شمارش', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('first-order', 'B11', 'مدارهای مرتبه اول', 'ورودی صفر، حالت صفر، فرمول طلایی، پاسخ پله و ضربه، انتگرال‌گیر', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('second-order', 'B12', 'مدارهای مرتبه دوم (RLC)', 'معادله مشخصه، چهار نوع پاسخ، جواب خصوصی، ضربه', 'فصل ۲ درس · کوییز III · میان‌ترم'),
        ('impulse', 'B13', 'پاسخ ضربه از روی معادله دیفرانسیل', 'تطبیق ضرایب ضربه، رابطه پاسخ پله و ضربه', 'فصل ۲ درس · میان‌ترم'),
        ('laplace', 'B14', 'کانولوشن و تبدیل لاپلاس', 'پاسخ به ورودی دلخواه، جدول تبدیل‌ها، قضایا، کسرهای جزئی', 'فصل ۳ درس · کوییز IV · میان‌ترم'),
        ('s-domain', 'B15', 'امپدانس، ادمیتانس و تحلیل در حوزه s', 'مدل المان‌ها با شرط اولیه، تابع شبکه، قطب و صفر، پایداری، حالت دائمی سینوسی', 'فصل ۳ درس · کوییز IV · میان‌ترم'),
    ]),
    ('C', 'الکترونیک دیجیتال', 'فصل‌های ۴ تا ۶ درس · پوشش پایان‌ترم', [
        ('diode', 'C1', 'دیود', 'نیمه‌هادی، پیوند p-n، مشخصه نمایی، مدل‌ها، یکسوساز، برش‌دهنده و زنر', 'فصل ۴ درس · کوییز V · پایان‌ترم'),
        ('mosfet', 'C2', 'ترانزیستور ماسفت افزایشی', 'ساختار، تشکیل کانال، نواحی کاری، مدل مداری و تحلیل DC', 'فصل ۴ درس · کوییز V · پایان‌ترم'),
        ('inverter', 'C3', 'وارونسازها و CMOS', 'بار مقاومتی و ترانزیستوری، CMOS، منحنی انتقال، حاشیه نویز، تأخیر و توان', 'فصل ۵ درس · کوییز V · پایان‌ترم'),
        ('pass-tg', 'C4', 'ترانزیستور گذر و دروازه انتقال', 'عبور ۰ و ۱، افت آستانه، گیت انتقال و طراحی منطق با آن', 'فصل ۵ درس · کوییز V · پایان‌ترم'),
        ('cmos-logic', 'C5', 'منطق CMOS ایستا و پویا', 'شبکه بالاکش و پایین‌کش، دوگانی، گیت پیچیده، اندازه‌گذاری، منطق دینامیک و دومینو', 'فصل ۵ درس · کوییز VI · پایان‌ترم'),
        ('latch-ff', 'C6', 'لچ، فلیپ‌فلاپ و شیفت رجیستر', 'لچ SR و D، معکوس‌کننده کلاک‌دار، Master–Slave، شیفت رجیستر دینامیک', 'فصل ۶ درس · کوییز VI · پایان‌ترم'),
        ('memory', 'C7', 'حافظه‌های RAM و ROM', 'آرایه، رمزگشا، PROM، EPROM، Flash، DRAM و SRAM', 'فصل ۶ درس · کوییز VI · پایان‌ترم'),
        ('converters', 'C8', 'نوسان‌ساز و مبدل‌های داده', 'نوسان‌ساز RC، مبدل D/A وزن‌دار و R-2R، مبدل‌های A/D', 'از جزوه کلاس'),
    ]),
    ('Z', 'پیوست', 'مرور مفهومی', [
        ('summary', 'Z1', 'نقشه مفهومی و جمع‌بندی روابط', 'هر رابطه با یک جمله «چرا»؛ برای مرور شب امتحان', 'مرور کل درس'),
    ]),
]

# Course schedule (from the course sheet), mapped to chapters.
SCHEDULE = [
    ('مهر ۵', 'المان‌های الکتریکی، قانون ولتاژ و جریان کیرشهف', ['elements', 'kirchhoff'], 'Quiz I'),
    ('مهر ۷', 'تحلیل مدار، اتصالات سری و موازی المان‌های مقاومتی', ['kirchhoff'], 'Quiz I'),
    ('مهر ۱۲', 'روش‌های تحلیل مدار: آنالیز گره و مش', ['nodal-mesh'], 'Quiz I'),
    ('مهر ۱۴', 'خطی بودن و اصل برهم‌نهی', ['thevenin'], 'Quiz I'),
    ('مهر ۱۹ تا ۲۶', 'مدارهای معادل تونن و نورتن', ['thevenin'], 'Quiz II'),
    ('مهر ۲۸', 'معرفی عناصر ذخیره‌کننده انرژی', ['capacitor', 'inductor'], 'Quiz III'),
    ('آبان ۳', 'شکل موج‌ها و مدارهای مرتبه اول', ['waveforms', 'switching', 'order', 'first-order'], 'Quiz III'),
    ('آبان ۱۰', 'مدارهای مرتبه اول', ['first-order'], 'Quiz III'),
    ('آبان ۱۲ و ۱۷', 'مدارهای مرتبه دوم', ['second-order', 'impulse'], 'Quiz III'),
    ('آبان ۱۹', 'امپدانس و ادمیتانس', ['s-domain'], 'Quiz IV'),
    ('آبان ۲۴ تا آذر ۱', 'آنالیز مدار با تبدیل لاپلاس', ['laplace', 's-domain'], 'Quiz IV'),
    ('آذر ۳ و ۸', 'منحنی مشخصه، مدل و کاربردهای دیود', ['diode'], 'Quiz V'),
    ('آذر ۱۰ و ۱۵', 'ساختار، عملکرد و منحنی مشخصه ماسفت افزایشی', ['mosfet'], 'Quiz V'),
    ('آذر ۱۷', 'انواع مدارهای وارونساز با ترانزیستور', ['inverter'], 'Quiz V'),
    ('آذر ۲۲ و ۲۴', 'ترانزیستور گذر و دروازه انتقال', ['pass-tg'], 'Quiz V'),
    ('آذر ۲۹', 'منطق CMOS ایستا', ['cmos-logic'], 'Quiz VI'),
    ('دی ۱ و ۶', 'Latch و FF، شیفت رجیستر', ['latch-ff'], 'Quiz VI'),
    ('دی ۸', 'انواع حافظه‌های RAM و ROM', ['memory'], 'Quiz VI'),
]

BOX = {
    'def': ('def', 'تعریف'),
    'int': ('int', 'شهود'),
    'prf': ('prf', 'اثبات قدم‌به‌قدم'),
    'note': ('note', 'نکته'),
    'trap': ('trap', 'دام رایج'),
    'key': ('key', 'نتیجه کلیدی'),
    'sum': ('sum', 'جمع‌بندی'),
    'phys': ('phys', 'فیزیکش چیست؟'),
}
LVL = {'1': 'پایه', '2': 'متوسط', '3': 'سخت', '4': 'چالشی'}

ATTR_RE = re.compile(r'(\w+)(?:="([^"]*)")?')


def attrs(s):
    return {k: (v if v is not None else True) for k, v in ATTR_RE.findall(s or '')}


def lvl_html(l):
    return '<span class="lvl" data-l="%s" title="سطح: %s"><i></i><i></i><i></i><i></i><span class="lt">%s</span></span>' % (l, LVL[l], LVL[l])


class BuildError(Exception):
    pass


def protect_math(s):
    def fix(m):
        return m.group(0).replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\\\[.*?\\\]', fix, s, flags=re.S)
    s = re.sub(r'\\\(.*?\\\)', fix, s, flags=re.S)
    return s


def expand(body, route, code, svgs):
    """Expand the shorthand tags of a chapter body."""
    # plots first (JSON may contain < or >)
    def plot(m):
        raw = m.group(1).strip()
        try:
            spec = json.loads(raw)
        except json.JSONDecodeError as e:
            raise BuildError('%s: bad plot JSON (%s): %s' % (route, e, raw[:120]))
        cap = spec.pop('cap', '')
        return '<figure class="plot" data-plot="%s">%s</figure>' % (
            html.escape(json.dumps(spec, ensure_ascii=False), quote=True),
            '<figcaption>%s</figcaption>' % cap if cap else '<figcaption></figcaption>')
    body = re.sub(r'<plot>(.*?)</plot>', plot, body, flags=re.S)
    body = protect_math(body)

    def fig(m):
        a = attrs(m.group(1))
        name = a.get('c')
        if name not in ck.REG:
            raise BuildError('%s: unknown circuit %r' % (route, name))
        if name not in svgs:
            svgs[name] = ck.to_svg(ck.REG[name](), float(a.get('s', 1.3)))
        cap = a.get('cap', '')
        return '<figure class="ckt"><div class="cv">%s</div>%s</figure>' % (svgs[name], '<figcaption>%s</figcaption>' % cap if cap else '')
    body = re.sub(r'<fig\s([^>]*?)/?>', fig, body)
    body = re.sub(r'<widget\s+w="([\w-]+)"\s*/?>', r'<div class="widget" data-w="\1"></div>', body)

    # balanced-tag check
    for t in list(BOX) + ['ex', 'sol', 'hw', 'ans', 'eq', 'steps']:
        o = len(re.findall(r'<%s(?:\s[^>]*)?>' % t, body))
        c = len(re.findall(r'</%s>' % t, body))
        if o != c:
            raise BuildError('%s: <%s> opened %d times, closed %d times' % (route, t, o, c))

    for t, (cls, label) in BOX.items():
        def box(m, cls=cls, label=label):
            a = attrs(m.group(1))
            title = a.get('t', '')
            lab = a.get('l', label)
            return '<div class="box %s"><div class="box-h"><span class="tag">%s</span>%s</div><div class="box-b">' % (
                cls, lab, '<span class="bt">%s</span>' % title if title else '')
        body = re.sub(r'<%s(\s[^>]*)?>' % t, box, body)
        body = body.replace('</%s>' % t, '</div></div>')

    cnt = {'ex': 0, 'hw': 0}

    def ex(m):
        a = attrs(m.group(1))
        cnt['ex'] += 1
        l = a.get('lvl', '1')
        return ('<div class="ex" id="%s-ex%d"><div class="ex-h"><span class="ex-n">مثال %s.%d</span><span class="ex-t">%s</span>%s</div><div class="ex-b">'
                % (route, cnt['ex'], code, cnt['ex'], a.get('t', ''), lvl_html(l)))
    body = re.sub(r'<ex(\s[^>]*)?>', ex, body)
    body = body.replace('</ex>', '</div></div>')
    body = re.sub(r'<sol(\s[^>]*)?>', lambda m: '<div class="sol"><div class="sol-h">%s</div>' % attrs(m.group(1)).get('t', 'حل گام‌به‌گام'), body)
    body = body.replace('</sol>', '</div>')

    def hw(m):
        a = attrs(m.group(1))
        cnt['hw'] += 1
        l = a.get('lvl', '2')
        return '<div class="hw" id="%s-hw%d"><div class="hw-h"><span class="hw-n">تمرین %s.%d</span>%s</div><div class="hw-b">' % (route, cnt['hw'], code, cnt['hw'], lvl_html(l))
    body = re.sub(r'<hw(\s[^>]*)?>', hw, body)
    body = body.replace('</hw>', '</div></div>')
    body = re.sub(r'<ans(\s[^>]*)?>', '<details class="ans"><summary>جواب و راهنمایی</summary><div>', body)
    body = body.replace('</ans>', '</div></details>')

    body = re.sub(r'<eq\s+k\s*>', '<div class="eq k"><span class="eq-l">رابطه کلیدی</span>', body)
    body = re.sub(r'<eq(\s[^>]*)?>', '<div class="eq">', body)
    body = body.replace('</eq>', '</div>')
    body = body.replace('<steps>', '<ol class="steps">').replace('</steps>', '</ol>')

    # headings
    secs = []

    def h2(m):
        secs.append(m.group(1))
        i = len(secs)
        return '<h2 id="%s-s%d"><span class="sn">%s.%d</span>%s</h2>' % (route, i, code, i, m.group(1))
    body = re.sub(r'<h2>(.*?)</h2>', h2, body, flags=re.S)
    h3n = {'n': 0}

    def h3(m):
        h3n['n'] += 1
        return '<h3 id="%s-h%d">%s</h3>' % (route, h3n['n'], m.group(1))
    body = re.sub(r'<h3>(.*?)</h3>', h3, body, flags=re.S)

    leftovers = re.findall(r'</?(?:def|int|prf|note|trap|key|sum|phys|ex|sol|hw|ans|eq|steps|fig|plot|widget|goals|prereq)\b', body)
    if leftovers:
        raise BuildError('%s: unexpanded tags %s' % (route, leftovers[:5]))
    return body, secs, cnt


TRACE = ('<svg class="trace" viewBox="0 0 600 18" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M0 9 H170 L180 3 H330 L340 15 H600" style="fill:none;stroke:var(--copper);stroke-width:2"/>'
         '<circle cx="170" cy="9" r="3.4" style="fill:var(--sheet);stroke:var(--copper);stroke-width:2"/>'
         '<circle cx="340" cy="15" r="3.4" style="fill:var(--sheet);stroke:var(--copper);stroke-width:2"/></svg>')

BRAND_ICON = ('<svg width="30" height="30" viewBox="0 0 30 30" aria-hidden="true">'
              '<rect x="1" y="1" width="28" height="28" rx="7" style="fill:var(--mask)"/>'
              '<path d="M5 15 H12.5 M12.5 8 V22 M17.5 8 V22 M17.5 15 H25" style="fill:none;stroke:var(--sheet);stroke-width:2.2;stroke-linecap:round"/></svg>')


def build_chapter(route, code, title, desc, cov, prev, nxt, svgs, titles):
    path = SRC / 'chapters' / (route + '.html')
    if not path.exists():
        return None
    raw = path.read_text(encoding='utf-8')
    goals = re.search(r'<goals>(.*?)</goals>', raw, re.S)
    prereq = re.search(r'<prereq>(.*?)</prereq>', raw, re.S)
    raw = re.sub(r'<goals>.*?</goals>', '', raw, flags=re.S)
    raw = re.sub(r'<prereq>.*?</prereq>', '', raw, flags=re.S)
    body, secs, cnt = expand(raw, route, code, svgs)

    pre_html = ''
    if prereq:
        links = []
        for r in prereq.group(1).split():
            if r not in titles:
                raise BuildError('%s: unknown prereq %r' % (route, r))
            links.append('<a href="#%s">%s · %s</a>' % (r, titles[r][0], titles[r][1]))
        pre_html = '<div class="chips">%s</div>' % ''.join(links)
    else:
        pre_html = '<p class="mut small" style="margin:0">پیش‌نیاز خاصی ندارد؛ از همین‌جا شروع کنید.</p>'
    hero = ('<header class="ch-hero"><span class="code">%s · %s</span><h1>%s</h1><p class="sub">%s</p>%s'
            '<div class="goals"><div class="gbox"><h4>در این فصل چه چیزی را واقعاً می‌فهمیم</h4><ul>%s</ul></div>'
            '<div class="gbox"><h4>پیش‌نیاز</h4>%s<h4 style="margin-top:10px">جایگاه در درس</h4><p style="margin:0">%s</p></div></div>'
            '<nav class="toc" aria-label="فهرست این فصل"><b>بخش‌های این فصل</b><ol>%s</ol></nav></header>') % (
        code, 'CHAPTER', title, desc, TRACE, goals.group(1) if goals else '', pre_html, cov,
        ''.join('<li><a href="#%s-s%d"><span class="sn">%s.%d</span>%s</a></li>' % (route, i + 1, code, i + 1, re.sub('<[^>]+>', '', s)) for i, s in enumerate(secs)))
    pn = '<nav class="pn" aria-label="فصل قبلی و بعدی">'
    if prev:
        pn += '<a class="prev" href="#%s"><span class="k">→ فصل قبل</span><span class="t">%s · %s</span></a>' % (prev[0], prev[1], prev[2])
    if nxt:
        pn += '<a class="next" href="#%s"><span class="k">فصل بعد ←</span><span class="t">%s · %s</span></a>' % (nxt[0], nxt[1], nxt[2])
    pn += '</nav>'
    art = '<article class="page chapter" data-route="%s" data-title="%s" hidden>%s<div class="prose">%s</div>%s</article>' % (
        route, html.escape(title), hero, body, pn)
    return art, secs, cnt


def build(artifact=False):
    for f in sorted((SRC / 'circuits').glob('*.py')):
        spec = importlib.util.spec_from_file_location('circ_' + f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

    flat = [(r, c, t, d, cov) for _, _, _, chs in PARTS for (r, c, t, d, cov) in chs]
    titles = {r: (c, t) for r, c, t, d, cov in flat}
    svgs = {}
    articles, nav_secs, built = [], {}, set()
    totals = {'ex': 0, 'hw': 0, 'ch': 0}
    available = [x for x in flat if (SRC / 'chapters' / (x[0] + '.html')).exists()]
    for i, (r, c, t, d, cov) in enumerate(available):
        prev = available[i - 1][:3] if i > 0 else None
        nxt = available[i + 1][:3] if i + 1 < len(available) else None
        res = build_chapter(r, c, t, d, cov, prev, nxt, svgs, titles)
        art, secs, cnt = res
        articles.append(art)
        nav_secs[r] = secs
        built.add(r)
        totals['ex'] += cnt['ex']
        totals['hw'] += cnt['hw']
        totals['ch'] += 1

    # ---- navigation ----
    nav = ['<input class="search" id="search" type="search" placeholder="جستجو در فصل‌ها و بخش‌ها…" aria-label="جستجو در فصل‌ها و بخش‌ها">',
           '<div class="nav-part"><a class="nav-ch" href="#home"><span class="cc">00</span><span>صفحه اول، برنامه درس و راهنما</span></a></div>']
    for pc, pt, pd, chs in PARTS:
        items = []
        for r, c, t, d, cov in chs:
            if r not in built:
                continue
            secs = ''.join('<a href="#%s-s%d"><span class="sn">%s.%d</span>%s</a>' % (r, i + 1, c, i + 1, re.sub('<[^>]+>', '', s)) for i, s in enumerate(nav_secs[r]))
            items.append('<div class="nav-item"><a class="nav-ch" href="#%s"><span class="cc">%s</span><span>%s</span></a><div class="nav-secs" hidden>%s</div></div>' % (r, c, t, secs))
        if items:
            nav.append('<div class="nav-part"><div class="ph"><span class="pc">%s</span>%s</div>%s</div>' % (pc, pt, ''.join(items)))

    # ---- home ----
    cards = []
    for pc, pt, pd, chs in PARTS:
        cs = ''.join('<a class="card" href="#%s"><span class="cc">%s</span><span class="ct">%s</span><span class="cd">%s</span></a>' % (r, c, t, d)
                     for r, c, t, d, cov in chs if r in built)
        if cs:
            cards.append('<div class="part-block"><div class="ph"><span class="pc">%s</span><h3>%s</h3><p>%s</p></div><div class="cards">%s</div></div>' % (pc, pt, pd, cs))
    sched_rows = ''.join('<tr><td style="white-space:nowrap">%s</td><td>%s</td><td>%s</td><td class="n">%s</td></tr>' % (
        dt, tp, ' '.join('<a href="#%s">%s</a>' % (r, titles[r][0]) for r in rs if r in built) or '—', q) for dt, tp, rs, q in SCHEDULE)
    home = HOME.format(nch=fa(totals['ch']), nex=fa(totals['ex']), nhw=fa(totals['hw']), nfig=fa(len(svgs)),
                       cards=''.join(cards), sched=sched_rows)

    css = (SRC / 'style.css').read_text(encoding='utf-8')
    js = (SRC / 'app.js').read_text(encoding='utf-8')
    head = ('<title>جزوه مدار و الکترونیک دیجیتال</title>\n'
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<meta name="description" content="جزوه کامل و قدم‌به‌قدم مدارهای الکتریکی و الکترونیک دیجیتال (پاییز ۱۴۰۵) با پایه‌های ریاضی، اثبات‌ها، شهود و مثال‌های حل‌شده">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Lalezar&family=Vazirmatn:wght@400;500;700;800&display=swap">\n'
            '<style>\n' + css + '\n</style>\n')
    shell = ('<div id="app" dir="rtl" lang="fa">'
             '<header class="topbar"><button class="iconbtn" id="navbtn" type="button" aria-label="باز کردن فهرست فصل‌ها"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h12" style="stroke:currentColor;stroke-width:1.8;stroke-linecap:round"/></svg>فهرست</button>'
             '<a class="brand" href="#home">' + BRAND_ICON + '<span style="display:flex;flex-direction:column;min-width:0"><span class="bt">جزوه مدار و الکترونیک دیجیتال</span><span class="bs">پاییز ۱۴۰۵ · از پایه تا شاقول</span></span></a>'
             '<span class="sp"></span><button class="iconbtn" id="themebtn" type="button" aria-label="تغییر حالت روشن و تیره"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" style="fill:none;stroke:currentColor;stroke-width:1.6"/><path d="M8 1.5 A6.5 6.5 0 0 1 8 14.5 Z" style="fill:currentColor"/></svg><span>روشن/تیره</span></button></header>'
             '<div class="shell"><aside class="side" id="side" aria-label="فهرست فصل‌ها">' + ''.join(nav) + '</aside>'
             '<main id="main">' + home + ''.join(articles) + '</main></div></div>\n'
             '<script>\n' + js + '\n</script>\n')
    if artifact:
        return head + shell
    return ('<!doctype html>\n<html lang="fa" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + shell + '</body>\n</html>\n'), totals, len(svgs)


HOME = '''<article class="page" data-route="home" data-title="">
<section class="cover">
  <span class="eyebrow">EEC · FALL 1405 · COMPLETE NOTES</span>
  <h1>مدارهای الکتریکی و الکترونیک دیجیتال<br><em>از پایه تا شاقول</em></h1>
  <p class="lead">جزوه‌ای که هیچ چیزی را بدیهی فرض نمی‌کند: از «شیب یک خط» و «بار الکتریکی» شروع می‌کند، هر رابطه را قدم‌به‌قدم استخراج می‌کند، اول شهودش را می‌گوید و بعد ریاضی‌اش را، و برای هر مبحث مثال تازه از پایه تا سخت حل می‌کند.</p>
  <div class="facts"><span><b>{nch}</b> فصل</span><span><b>{nex}</b> مثال حل‌شده</span><span><b>{nhw}</b> تمرین با جواب</span><span><b>{nfig}</b> شکل مدار</span><span>منبع: جزوه‌های کلاس و برنامه ترم</span></div>
  <svg class="trace" viewBox="0 0 800 70" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0 52 H120 L140 32 H300 L318 50 H420 L440 30 H520 L540 50 H800" style="fill:none;stroke:var(--copper);stroke-width:2.2"/>
    <path d="M0 62 H210 L226 46 H600 L616 62 H800" style="fill:none;stroke:var(--mask);stroke-width:1.6;opacity:.7"/>
    <circle cx="120" cy="52" r="5" style="fill:var(--sheet);stroke:var(--copper);stroke-width:2.2"/><circle cx="420" cy="50" r="5" style="fill:var(--sheet);stroke:var(--copper);stroke-width:2.2"/>
    <circle cx="226" cy="46" r="4" style="fill:var(--sheet);stroke:var(--mask);stroke-width:1.6"/><circle cx="616" cy="62" r="4" style="fill:var(--sheet);stroke:var(--mask);stroke-width:1.6"/>
  </svg>
</section>

<section class="howto">
  <h2>این جزوه را چطور بخوانیم</h2>
  <p>هر نوع مطلب رنگ خودش را دارد تا قبل از خواندن بدانید با چه چیزی روبه‌رو هستید. اگر عجله دارید، فقط جعبه‌های «شهود» و «نتیجه کلیدی» را بخوانید؛ اگر می‌خواهید واقعاً بفهمید، «اثبات قدم‌به‌قدم» را با مداد و کاغذ دنبال کنید.</p>
  <div class="legend">
    <div class="lg" style="--k:var(--c-def)"><b>تعریف</b><span>معنی دقیق یک کلمه؛ همه‌چیز بعداً روی همین ساخته می‌شود.</span></div>
    <div class="lg" style="--k:var(--c-int)"><b>شهود</b><span>تصویر ذهنی: چرا این رابطه منطقی است، بدون فرمول.</span></div>
    <div class="lg" style="--k:var(--c-prf)"><b>اثبات</b><span>استخراج رابطه، یک قدم در هر خط، بدون پرش.</span></div>
    <div class="lg" style="--k:var(--copper)"><b>نتیجه کلیدی</b><span>چیزی که باید بفهمید (نه حفظ کنید) و همه‌جا به کار می‌آید.</span></div>
    <div class="lg" style="--k:var(--c-trap)"><b>دام رایج</b><span>اشتباهی که بیشتر دانشجوها در امتحان می‌کنند.</span></div>
    <div class="lg" style="--k:var(--c-ex)"><b>مثال</b><span>با نوار سطح: ▮ پایه، ▮▮ متوسط، ▮▮▮ سخت، ▮▮▮▮ چالشی.</span></div>
    <div class="lg" style="--k:var(--c-hw)"><b>تمرین</b><span>اول خودتان حل کنید، بعد جواب را باز کنید.</span></div>
    <div class="lg" style="--k:var(--c-phys)"><b>فیزیکش چیست؟</b><span>آنچه واقعاً درون قطعه اتفاق می‌افتد.</span></div>
  </div>
  <p class="small mut" style="margin-top:10px">قراردادهای ثابت کل جزوه: جهت مرجع جریان از سر + ولتاژ وارد المان می‌شود (قرارداد علامت غیرفعال)؛ ولتاژ هر گره نسبت به گره زمین سنجیده می‌شود؛ 0⁻ و 0⁺ یعنی درست قبل و درست بعد از کلیدزنی در t = 0؛ u(t) پله واحد و δ(t) ضربه واحد است.</p>
</section>

<section class="roadmap">
  <h2>برنامه ترم و نقشه مطالعه</h2>
  <p>جدول زیر از برنامه رسمی درس آمده است. ستون سوم فصل‌های این جزوه را نشان می‌دهد که آن جلسه را پوشش می‌دهند. نمره از ۲۰: میان‌ترم ۵، پایان‌ترم ۷، کوییزها ۴، تمرین‌ها ۴. میان‌ترم فصل‌های ۱ تا ۳ درس (بخش B) و پایان‌ترم فصل‌های ۴ تا ۶ (بخش C) را می‌پوشاند.</p>
  <div class="tbl"><table><thead><tr><th>جلسه</th><th>مبحث</th><th>فصل جزوه</th><th class="n">کوییز</th></tr></thead><tbody>{sched}</tbody></table></div>
  <p class="small mut">اگر پایه ریاضی‌تان لرزان است، قبل از بخش B فصل‌های بخش A را بخوانید؛ هر فصل در ابتدایش پیش‌نیازهایش را با لینک نوشته است.</p>
  {cards}
</section>
<p class="foot">این جزوه بر اساس جزوه‌های کلاس درس «مدارهای الکتریکی و الکترونیک دیجیتال» و برنامه ترم پاییز ۱۴۰۵ بازنویسی و کامل شده است. مثال‌ها تازه‌اند و همه حل‌ها قدم‌به‌قدم بازبینی شده‌اند.</p>
</article>'''


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--artifact':
        out = pathlib.Path(sys.argv[2])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(artifact=True), encoding='utf-8')
        print('artifact ->', out, out.stat().st_size, 'bytes')
    else:
        doc, totals, nfig = build()
        (ROOT / 'docs').mkdir(exist_ok=True)
        (ROOT / 'docs' / 'index.html').write_text(doc, encoding='utf-8')
        (ROOT / 'docs' / '.nojekyll').write_text('', encoding='utf-8')
        print('docs/index.html', len(doc.encode('utf-8')), 'bytes;', totals, 'circuits:', nfig)
