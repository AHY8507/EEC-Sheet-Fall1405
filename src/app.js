(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = document.documentElement;
  var pages = $$('article.page');
  var byRoute = {};
  pages.forEach(function (p) { byRoute[p.dataset.route] = p; });
  var current = null, pendingTarget = null, mjReady = false;
  var PRINT = root.classList.contains('print'); // one long document for the PDF build

  /* ---------------- theme ---------------- */
  try { var saved = localStorage.getItem('eec-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  var themeBtn = $('#themebtn');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var isDark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    var t = isDark ? 'light' : 'dark';
    root.setAttribute('data-theme', t);
    try { localStorage.setItem('eec-theme', t); } catch (e) {}
  });

  /* ---------------- nav drawer ---------------- */
  var scrim = null;
  function closeNav() { document.body.classList.remove('nav-open'); if (scrim) { scrim.remove(); scrim = null; } }
  var navBtn = $('#navbtn');
  if (navBtn) navBtn.addEventListener('click', function () {
    if (document.body.classList.contains('nav-open')) { closeNav(); return; }
    document.body.classList.add('nav-open');
    scrim = document.createElement('div'); scrim.className = 'scrim'; scrim.addEventListener('click', closeNav);
    document.body.appendChild(scrim);
  });

  /* ---------------- search ---------------- */
  function norm(s) { return (s || '').replace(/ي/g, 'ی').replace(/ك/g, 'ک').replace(/‌/g, ' ').toLowerCase(); }
  var search = $('#search');
  function applySearch() {
    var q = norm(search ? search.value.trim() : '');
    $$('.nav-item').forEach(function (it) {
      var ch = $('.nav-ch', it), secs = $('.nav-secs', it);
      if (!q) {
        it.hidden = false;
        if (secs) { secs.hidden = !ch.classList.contains('on'); $$('a', secs).forEach(function (a) { a.hidden = false; }); }
        return;
      }
      var chMatch = norm(ch.textContent).indexOf(q) >= 0, anySec = false;
      if (secs) $$('a', secs).forEach(function (a) { var m = norm(a.textContent).indexOf(q) >= 0; a.hidden = !m && !chMatch; if (m) anySec = true; });
      it.hidden = !(chMatch || anySec);
      if (secs) secs.hidden = !(anySec || chMatch);
    });
    $$('.nav-part').forEach(function (p) { p.hidden = $$('.nav-item', p).every(function (i) { return i.hidden; }); });
  }
  if (search) search.addEventListener('input', applySearch);

  /* ---------------- router ---------------- */
  function updateNav() {
    var r = current ? current.dataset.route : '';
    $$('.nav-ch').forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + r); if (a.classList.contains('on')) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
    applySearch();
    var on = $('.nav-ch.on');
    if (on && on.scrollIntoView) { try { on.scrollIntoView({ block: 'nearest' }); } catch (e) {} }
    document.title = (current && current.dataset.title ? current.dataset.title + ' · ' : '') + 'جزوه مدار و الکترونیک دیجیتال';
  }
  function route() {
    var h = '';
    try { h = decodeURIComponent(location.hash.slice(1)); } catch (e) { h = location.hash.slice(1); }
    var page = byRoute[h], target = null;
    if (!page && h) { var el = document.getElementById(h); if (el) { page = el.closest('article.page'); target = el; } }
    if (!page) page = byRoute.home;
    if (page !== current) {
      pages.forEach(function (p) { p.hidden = p !== page; });
      current = page; updateNav(); renderPage(page);
      if (!target) window.scrollTo(0, 0);
    }
    if (target) { pendingTarget = target; target.scrollIntoView(); }
    closeNav();
  }
  window.addEventListener('hashchange', route);

  function renderPage(p) {
    $$('figure.plot', p).forEach(drawPlotFigure);
    $$('.widget', p).forEach(initWidget);
    typeset(p);
  }

  /* ---------------- MathJax (lazy, per page) ---------------- */
  window.MathJax = {
    tex: { inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']], tags: 'none' },
    svg: { fontCache: 'global' },
    options: { enableMenu: false },
    startup: {
      typeset: false,
      ready: function () {
        window.MathJax.startup.defaultReady(); mjReady = true;
        if (PRINT) {
          window.MathJax.typesetPromise([document.getElementById('main')])
            .then(function () { root.dataset.mj = 'done'; }, function (e) { root.dataset.mj = 'error: ' + e; });
          return;
        }
        if (current) typeset(current);
      }
    }
  };
  function typeset(p) {
    if (!mjReady || !p || p.dataset.mj) return;
    p.dataset.mj = '1';
    window.MathJax.typesetPromise([p]).then(function () {
      if (pendingTarget && current && current.contains(pendingTarget)) { pendingTarget.scrollIntoView(); }
      pendingTarget = null;
    }).catch(function () {});
  }
  function loadMJ(srcs) {
    var s = document.createElement('script');
    s.src = srcs[0]; s.async = true;
    s.onerror = function () { s.remove(); if (srcs.length > 1) loadMJ(srcs.slice(1)); };
    (document.head || document.body).appendChild(s);
  }
  loadMJ(['https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js',
          'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js',
          'https://unpkg.com/mathjax@3.2.2/es5/tex-svg.js']);

  /* ---------------- plotting ---------------- */
  var COL = ['var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)', 'var(--c5)', 'var(--c6)'];
  var uid = 0;
  function niceStep(range, n) { var raw = range / n, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p; return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p; }
  function autoTicks(a, b, n) { var s = niceStep(b - a, n || 5), out = []; for (var v = Math.ceil(a / s - 1e-9) * s; v <= b + 1e-9; v += s) out.push(+v.toFixed(10)); return out; }
  function fmt(v) { if (typeof v === 'string') return v; var a = Math.abs(v); if (a !== 0 && (a >= 1e5 || a < 1e-3)) return v.toExponential(0); return String(+v.toFixed(3)); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var fnCache = {};
  function compile(expr) {
    if (fnCache[expr]) return fnCache[expr];
    var f = new Function('x', 'var M=Math,exp=M.exp,sin=M.sin,cos=M.cos,tan=M.tan,sqrt=M.sqrt,abs=M.abs,log=M.log,PI=M.PI,max=M.max,min=M.min,pow=M.pow,floor=M.floor,atan=M.atan,sinh=M.sinh,cosh=M.cosh,sign=M.sign,E=M.E;' +
      'var u=function(t){return t>=0?1:0};var rect=function(t,a,b){return (t>=a&&t<b)?1:0};var mod=function(a,b){return ((a%b)+b)%b};return (' + expr + ');');
    fnCache[expr] = f; return f;
  }
  function panelSVG(p, W, h, y0, last) {
    var m = { l: 58, r: 18, t: 24, b: last ? 36 : 14 };
    var x0 = p.x[0], x1 = p.x[1], ya = p.y[0], yb = p.y[1];
    var L = m.l, R = W - m.r, T = y0 + m.t, B = y0 + m.t + h;
    var sx = function (x) { return L + (x - x0) / (x1 - x0) * (R - L); };
    var sy = function (v) { return B - (v - ya) / (yb - ya) * (B - T); };
    var xt = p.xt || autoTicks(x0, x1, 6), yt = p.yt || autoTicks(ya, yb, 4);
    var o = '', id = 'clp' + (++uid);
    o += '<defs><clipPath id="' + id + '"><rect x="' + L + '" y="' + (T - 2) + '" width="' + (R - L) + '" height="' + (B - T + 4) + '"/></clipPath></defs>';
    xt.forEach(function (t) { var X = sx(t); o += '<line class="gr" x1="' + X + '" x2="' + X + '" y1="' + T + '" y2="' + B + '"/>'; if (last) o += '<text class="tk" x="' + X + '" y="' + (B + 16) + '" text-anchor="middle">' + esc(fmt(t)) + '</text>'; });
    yt.forEach(function (t) { var Y = sy(t); o += '<line class="gr" x1="' + L + '" x2="' + R + '" y1="' + Y + '" y2="' + Y + '"/><text class="tk" x="' + (L - 7) + '" y="' + (Y + 4) + '" text-anchor="end">' + esc(fmt(t)) + '</text>'; });
    var axY = (ya <= 0 && yb >= 0) ? sy(0) : B;
    o += '<line class="ax" x1="' + L + '" x2="' + R + '" y1="' + axY + '" y2="' + axY + '"/>';
    var axX = (x0 <= 0 && x1 >= 0) ? sx(0) : L;
    o += '<line class="ax" x1="' + axX + '" x2="' + axX + '" y1="' + T + '" y2="' + B + '"/>';
    (p.vx || []).forEach(function (v) { var X = sx(v); o += '<line class="guide" x1="' + X + '" x2="' + X + '" y1="' + T + '" y2="' + B + '"/>'; });
    (p.hy || []).forEach(function (v) { var Y = sy(v); o += '<line class="guide" x1="' + L + '" x2="' + R + '" y1="' + Y + '" y2="' + Y + '"/>'; });
    o += '<g clip-path="url(#' + id + ')">';
    (p.fill || []).forEach(function (c) { // shaded area under expr between a,b
      var f = compile(c.f), N = 200, a = c.r[0], b = c.r[1], d = 'M' + sx(a) + ',' + sy(0);
      for (var i = 0; i <= N; i++) { var x = a + (b - a) * i / N, y = f(x); d += 'L' + sx(x).toFixed(2) + ',' + sy(y).toFixed(2); }
      d += 'L' + sx(b) + ',' + sy(0) + 'Z';
      o += '<path d="' + d + '" style="fill:' + COL[(c.k || 1) - 1] + ';fill-opacity:.16;stroke:none"/>';
    });
    (p.c || []).forEach(function (c) {
      var col = COL[(c.k || 1) - 1], w = c.w || 2.2, d = '';
      if (c.f) {
        var f = compile(c.f), a = c.r ? c.r[0] : x0, b = c.r ? c.r[1] : x1, N = c.n || 700, pen = false;
        for (var i = 0; i <= N; i++) {
          var x = a + (b - a) * i / N, y;
          try { y = f(x); } catch (e) { y = NaN; }
          if (!isFinite(y) || Math.abs(y) > 1e6) { pen = false; continue; }
          d += (pen ? 'L' : 'M') + sx(x).toFixed(2) + ',' + sy(y).toFixed(2); pen = true;
        }
      } else if (c.p) {
        c.p.forEach(function (pt, i) { d += (i ? 'L' : 'M') + sx(pt[0]).toFixed(2) + ',' + sy(pt[1]).toFixed(2); });
      }
      o += '<path d="' + d + '" style="fill:none;stroke:' + col + ';stroke-width:' + w + ';stroke-linejoin:round;stroke-linecap:round' + (c.d ? ';stroke-dasharray:6 5' : '') + '"/>';
      (c.arrows || []).forEach(function (ar) { // impulse arrows [x, height]
        var X = sx(ar[0]), Y0 = sy(0), Y1 = sy(ar[1]);
        o += '<line x1="' + X + '" x2="' + X + '" y1="' + Y0 + '" y2="' + Y1 + '" style="stroke:' + col + ';stroke-width:' + w + '"/>' +
          '<path d="M' + (X - 5) + ',' + (Y1 + (ar[1] > 0 ? 9 : -9)) + 'L' + X + ',' + Y1 + 'L' + (X + 5) + ',' + (Y1 + (ar[1] > 0 ? 9 : -9)) + '" style="fill:none;stroke:' + col + ';stroke-width:' + w + '"/>';
        if (ar[2]) o += '<text class="an" x="' + (X + 7) + '" y="' + (Y1 + 4) + '">' + esc(ar[2]) + '</text>';
      });
    });
    o += '</g>';
    (p.pts || []).forEach(function (q) {
      var X = sx(q[0]), Y = sy(q[1]), anc = q[3] || 'start', dx = anc === 'end' ? -7 : anc === 'middle' ? 0 : 7, dy = q[4] != null ? q[4] : -7;
      o += '<circle cx="' + X + '" cy="' + Y + '" r="3.6" style="fill:var(--sheet);stroke:var(--ink);stroke-width:1.6"/>';
      if (q[2]) o += '<text class="an" x="' + (X + dx) + '" y="' + (Y + dy) + '" text-anchor="' + anc + '">' + esc(q[2]) + '</text>';
    });
    (p.txt || []).forEach(function (q) { o += '<text class="an" x="' + sx(q[0]) + '" y="' + sy(q[1]) + '" text-anchor="' + (q[3] || 'middle') + '"' + (q[4] ? ' style="fill:' + COL[q[4] - 1] + '"' : '') + '>' + esc(q[2]) + '</text>'; });
    if (p.yl) o += '<text class="al" x="' + (L - 50) + '" y="' + (T - 9) + '">' + esc(p.yl) + '</text>';
    if (p.xl && last) o += '<text class="al" x="' + R + '" y="' + (B + 32) + '" text-anchor="end">' + esc(p.xl) + '</text>';
    return { svg: o, H: m.t + h + m.b };
  }
  function plotSVG(spec) {
    var panels = spec.panels || [spec], W = spec.w || 640, ph = spec.ph || 210, y = 0, out = '';
    panels.forEach(function (pp, i) {
      var p = {}; for (var k in spec) if (k !== 'panels') p[k] = spec[k]; for (var k2 in pp) p[k2] = pp[k2];
      var r = panelSVG(p, W, pp.h || ph, y, i === panels.length - 1); out += r.svg; y += r.H;
    });
    return '<svg viewBox="0 0 ' + W + ' ' + y + '" role="img" aria-label="' + esc(spec.aria || 'نمودار') + '">' + out + '</svg>';
  }
  function legendHTML(spec) {
    var items = [];
    (spec.panels || [spec]).forEach(function (p) { (p.c || []).forEach(function (c) { if (c.name) items.push('<span style="--lc:' + COL[(c.k || 1) - 1] + '">' + esc(c.name) + '</span>'); }); });
    return items.length ? '<div class="plot-legend">' + items.join('') + '</div>' : '';
  }
  function drawPlotFigure(fig) {
    if (fig.dataset.done) return;
    var spec; try { spec = JSON.parse(fig.dataset.plot); } catch (e) { fig.insertAdjacentHTML('afterbegin', '<p class="mut">plot spec error</p>'); return; }
    fig.dataset.done = '1';
    var cap = fig.querySelector('figcaption');
    var div = document.createElement('div'); div.className = 'pv';
    try { div.innerHTML = plotSVG(spec) + legendHTML(spec); } catch (e) { div.textContent = 'plot error: ' + e.message; }
    fig.insertBefore(div, cap);
  }

  /* ---------------- widgets ---------------- */
  function slider(id, label, min, max, step, val, unit) {
    return '<label for="' + id + '">' + label + ' <span class="v" id="' + id + '-v"></span><input type="range" id="' + id + '" min="' + min + '" max="' + max + '" step="' + step + '" value="' + val + '"></label>';
  }
  function bind(w, ids, fn) {
    ids.forEach(function (id) { var el = $('#' + id, w); if (el) el.addEventListener('input', fn); });
    fn();
  }
  function val(w, id) { return parseFloat($('#' + id, w).value); }
  function show(w, id, txt) { var el = $('#' + id + '-v', w); if (el) el.textContent = txt; }
  function f2(v, d) { return (+v).toFixed(d == null ? 2 : d); }

  var WIDGETS = {
    tangent: function (w) {
      w.innerHTML = '<div class="wt">آزمایشگاه شیب: از وتر تا مماس</div><p class="wd">نقطه P را جابه‌جا کنید و فاصله h را کوچک کنید. خط نارنجی (وتر) از P و Q می‌گذرد. وقتی h به صفر نزدیک می‌شود، وتر روی خط‌چین (مماس) می‌خوابد و شیبش به «مشتق» می‌رسد. تابع: <span class="ltr">f(x) = x²/4 + 1</span></p>' +
        '<div class="ctrls">' + slider('tg-x', 'محل نقطه P (x₀)', 0.5, 5, 0.05, 2) + slider('tg-h', 'فاصله h', 0.01, 3, 0.01, 2) + '</div><div class="sv"></div><div class="read"></div>';
      bind(w, ['tg-x', 'tg-h'], function () {
        var x0 = val(w, 'tg-x'), h = val(w, 'tg-h'), f = function (x) { return x * x / 4 + 1; };
        show(w, 'tg-x', f2(x0)); show(w, 'tg-h', f2(h));
        var ms = (f(x0 + h) - f(x0)) / h, md = x0 / 2;
        var sec = f(x0) + '+' + ms + '*(x-' + x0 + ')', tan = f(x0) + '+' + md + '*(x-' + x0 + ')';
        $('.sv', w).innerHTML = plotSVG({ x: [0, 8], y: [0, 14], xl: 'x', yl: 'f(x)', c: [{ f: 'x*x/4+1', k: 2 }, { f: tan, k: 6, d: 1, w: 1.6 }, { f: sec, k: 1, w: 2 }], pts: [[x0, f(x0), 'P', 'end'], [x0 + h, f(x0 + h), 'Q', 'start']] });
        $('.read', w).innerHTML = 'شیب وتر = Δy/Δx = <b>' + f2(ms, 4) + '</b> · شیب مماس (مشتق در x₀) = <b>' + f2(md, 4) + '</b> · اختلاف = <b>' + f2(ms - md, 4) + '</b> <span class="mut">(دقیقاً برابر h/4؛ با h→0 صفر می‌شود)</span>';
      });
    },
    riemann: function (w) {
      w.innerHTML = '<div class="wt">آزمایشگاه انتگرال: بار = مساحت زیر نمودار جریان</div><p class="wd">جریان <span class="ltr">i(t) = 1 + 0.5t + sin(2t)</span> آمپر است. بازه ۰ تا ۴ ثانیه را به n نوار باریک تقسیم می‌کنیم؛ در هر نوار جریان را تقریباً ثابت می‌گیریم و «جریان × مدت» را جمع می‌کنیم. هرچه n بزرگ‌تر، جمع به مقدار دقیق انتگرال نزدیک‌تر.</p>' +
        '<div class="ctrls">' + slider('rm-n', 'تعداد نوارها n', 1, 80, 1, 4) + '</div><div class="sv"></div><div class="read"></div>';
      bind(w, ['rm-n'], function () {
        var n = Math.round(val(w, 'rm-n')); show(w, 'rm-n', n);
        var f = function (t) { return 1 + 0.5 * t + Math.sin(2 * t); }, a = 0, b = 4, dt = (b - a) / n, s = 0, pts = [[0, 0]];
        for (var i = 0; i < n; i++) { var tm = a + (i + 0.5) * dt, y = f(tm); s += y * dt; pts.push([a + i * dt, y], [a + (i + 1) * dt, y], [a + (i + 1) * dt, 0]); }
        var exact = 8 - (Math.cos(8) - 1) / 2;
        $('.sv', w).innerHTML = plotSVG({ x: [0, 4], y: [0, 4.5], xl: 't (s)', yl: 'i (A)', c: [{ p: pts, k: 1, w: 1.4 }, { f: '1+0.5*x+sin(2*x)', k: 2 }] });
        $('.read', w).innerHTML = 'جمع مستطیل‌ها = <b>' + f2(s, 4) + ' C</b> · مقدار دقیق انتگرال = <b>' + f2(exact, 4) + ' C</b> · خطا = <b>' + f2(s - exact, 4) + '</b>';
      });
    },
    rc: function (w) {
      w.innerHTML = '<div class="wt">آزمایشگاه شارژ خازن (مدار RC با منبع پله)</div><p class="wd">در لحظه صفر کلید وصل می‌شود و خازن بی‌بار از طریق R شارژ می‌شود. R و C را عوض کنید و ببینید فقط حاصل‌ضرب آن‌ها (ثابت زمانی τ) سرعت را تعیین می‌کند.</p>' +
        '<div class="ctrls">' + slider('rc-r', 'مقاومت R (kΩ)', 1, 10, 0.5, 4) + slider('rc-c', 'ظرفیت C (µF)', 10, 50, 1, 25) + slider('rc-v', 'ولتاژ منبع Vs (V)', 1, 12, 0.5, 10) + '</div><div class="sv"></div><div class="read"></div>';
      bind(w, ['rc-r', 'rc-c', 'rc-v'], function () {
        var R = val(w, 'rc-r'), C = val(w, 'rc-c'), V = val(w, 'rc-v'), tau = R * C; // ms
        show(w, 'rc-r', f2(R, 1) + ' kΩ'); show(w, 'rc-c', C + ' µF'); show(w, 'rc-v', f2(V, 1) + ' V');
        $('.sv', w).innerHTML = plotSVG({ x: [0, 2500], panels: [
          { y: [0, 12.5], yt: [0, 4, 8, 12], yl: 'vC (V)', c: [{ f: V + '*(1-exp(-x/' + tau + '))', k: 1 }], vx: [tau, 5 * tau], hy: [0.632 * V], pts: [[tau, 0.632 * V, 'τ', 'start', 14]] },
          { y: [0, 12.5], yt: [0, 4, 8, 12], yl: 'i (mA)', h: 120, c: [{ f: (V / R) + '*exp(-x/' + tau + ')', k: 2 }], vx: [tau, 5 * tau] }
        ], xl: 't (ms)' });
        $('.read', w).innerHTML = 'τ = R·C = <b>' + f2(tau, 0) + ' ms</b> · جریان اولیه Vs/R = <b>' + f2(V / R) + ' mA</b> · در t = τ ولتاژ <b>' + f2(0.632 * V) + ' V</b> (۶۳٪) · بعد از ۵τ = <b>' + f2(5 * tau, 0) + ' ms</b> بیش از ۹۹٪ شارژ';
      });
    },
    rlc: function (w) {
      w.innerHTML = '<div class="wt">آزمایشگاه RLC سری: چهار رفتار با یک پیچ</div><p class="wd">L = 1H و C = 0.25F ثابت‌اند (پس ω₀ = 2 rad/s). در لحظه صفر ولتاژ پله 1V وصل می‌شود و ولتاژ خازن را می‌بینیم. فقط R را عوض کنید: R کم ⇒ نوسان، R = 4Ω ⇒ بحرانی، R زیاد ⇒ کند و بی‌نوسان.</p>' +
        '<div class="ctrls">' + slider('rl-r', 'مقاومت R (Ω)', 0, 10, 0.1, 1) + '</div><div class="sv"></div><div class="read"></div>';
      bind(w, ['rl-r'], function () {
        var R = val(w, 'rl-r'), L = 1, C = 0.25, a = R / (2 * L), w0 = 1 / Math.sqrt(L * C), f, kind, roots;
        show(w, 'rl-r', f2(R, 1) + ' Ω');
        if (Math.abs(a - w0) < 1e-3) { f = '1-(1+' + a + '*x)*exp(-' + a + '*x)'; kind = 'میرای بحرانی'; roots = 's₁ = s₂ = ' + f2(-a); }
        else if (a > w0) { var d = Math.sqrt(a * a - w0 * w0), s1 = -a + d, s2 = -a - d, A1 = s2 / (s1 - s2), A2 = -s1 / (s1 - s2); f = '1+(' + A1 + ')*exp(' + s1 + '*x)+(' + A2 + ')*exp(' + s2 + '*x)'; kind = 'فوق‌میرا'; roots = 's₁ = ' + f2(s1) + ' , s₂ = ' + f2(s2); }
        else { var wd = Math.sqrt(w0 * w0 - a * a); f = '1-exp(-' + a + '*x)*(cos(' + wd + '*x)+(' + (a / wd) + ')*sin(' + wd + '*x))'; kind = a === 0 ? 'بی‌اتلاف (نوسان دائمی)' : 'زیرمیرا (نوسانی)'; roots = 's = ' + f2(-a) + ' ± j' + f2(wd); }
        $('.sv', w).innerHTML = plotSVG({ x: [0, 12], y: [0, 2.1], yt: [0, 0.5, 1, 1.5, 2], xl: 't (s)', yl: 'vC (V)', hy: [1], c: [{ f: f, k: 1 }] });
        $('.read', w).innerHTML = '<span class="badge">' + kind + '</span> α = R/2L = <b>' + f2(a) + '</b> · ω₀ = <b>2</b> · ریشه‌ها: <b>' + roots + '</b> · R بحرانی = 2√(L/C) = <b>4 Ω</b>';
      });
    },
    phasor: function (w) {
      w.innerHTML = '<div class="wt">بردار چرخان و موج سینوسی</div><p class="wd">یک بردار به طول A با سرعت زاویه‌ای ثابت می‌چرخد. سایه آن روی محور عمودی، همان <span class="ltr">A·sin(θ)</span> است و سایه روی محور افقی <span class="ltr">A·cos(θ)</span>. زاویه را بچرخانید و نقطه روی موج را دنبال کنید.</p>' +
        '<div class="ctrls">' + slider('ph-t', 'زاویه θ (درجه)', 0, 720, 1, 60) + slider('ph-a', 'دامنه A', 0.5, 2, 0.1, 1.5) + '</div><div class="sv"></div><div class="read"></div>';
      bind(w, ['ph-t', 'ph-a'], function () {
        var th = val(w, 'ph-t'), A = val(w, 'ph-a'), r = th * Math.PI / 180;
        show(w, 'ph-t', th + '°'); show(w, 'ph-a', f2(A, 1));
        var cx = 120, cy = 130, S = 50, px = cx + S * A * Math.cos(r), py = cy - S * A * Math.sin(r);
        var o = '<svg viewBox="0 0 640 260" role="img" aria-label="بردار چرخان">';
        o += '<line class="gr" x1="10" x2="230" y1="' + cy + '" y2="' + cy + '"/><line class="gr" x1="' + cx + '" x2="' + cx + '" y1="20" y2="240"/>';
        o += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (S * A) + '" style="fill:none;stroke:var(--rule);stroke-width:1.5"/>';
        o += '<line x1="' + cx + '" y1="' + cy + '" x2="' + px + '" y2="' + py + '" style="stroke:var(--c1);stroke-width:3"/><circle cx="' + px + '" cy="' + py + '" r="4.5" style="fill:var(--c1)"/>';
        o += '<line class="guide" x1="' + px + '" y1="' + py + '" x2="' + px + '" y2="' + cy + '"/><line class="guide" x1="' + px + '" y1="' + py + '" x2="' + (260 + r / (4 * Math.PI) * 360) + '" y2="' + py + '"/>';
        o += '<line x1="' + cx + '" y1="' + cy + '" x2="' + px + '" y2="' + cy + '" style="stroke:var(--c2);stroke-width:3"/><line x1="' + px + '" y1="' + cy + '" x2="' + px + '" y2="' + py + '" style="stroke:var(--c3);stroke-width:3"/>';
        var d = ''; for (var i = 0; i <= 360; i++) { var t = i / 360 * 4 * Math.PI; d += (i ? 'L' : 'M') + (260 + i) + ',' + (cy - S * A * Math.sin(t)).toFixed(2); }
        o += '<line class="gr" x1="260" x2="625" y1="' + cy + '" y2="' + cy + '"/><path d="' + d + '" style="fill:none;stroke:var(--c3);stroke-width:2.2"/>';
        o += '<circle cx="' + (260 + r / (4 * Math.PI) * 360) + '" cy="' + py + '" r="4.5" style="fill:var(--c3)"/>';
        o += '<text class="tk" x="262" y="250">0</text><text class="tk" x="440" y="250" text-anchor="middle">2π</text><text class="tk" x="620" y="250" text-anchor="end">4π</text></svg>';
        $('.sv', w).innerHTML = o;
        $('.read', w).innerHTML = 'سایه افقی A·cos θ = <b>' + f2(A * Math.cos(r)) + '</b> <span class="mut">(آبی)</span> · سایه عمودی A·sin θ = <b>' + f2(A * Math.sin(r)) + '</b> <span class="mut">(سبز)</span> · به زبان مختلط: <b>A·e^{jθ} = ' + f2(A * Math.cos(r)) + ' + j' + f2(A * Math.sin(r)) + '</b>';
      });
    },
    sar: function (w) {
      w.innerHTML = '<div class="wt">مبدل تقریب متوالی (SAR) چهاربیتی، گام‌به‌گام</div><p class="wd">بازه ۰ تا ۱۶ ولت، هر LSB یک ولت. مبدل مثل بازی «حدس عدد» از پرارزش‌ترین بیت شروع می‌کند: بیت را ۱ می‌گذارد، خروجی D/A را با ورودی مقایسه می‌کند و اگر زیادی بود آن بیت را ۰ می‌کند.</p>' +
        '<div class="ctrls">' + slider('sar-v', 'ولتاژ ورودی Vin (V)', 0, 15.9, 0.1, 11.3) + '</div><div class="btns"><button class="iconbtn" id="sar-step" type="button">گام بعد</button><button class="iconbtn" id="sar-reset" type="button">شروع دوباره</button></div><div class="sv"></div><div class="read"></div>';
      var k = PRINT ? 4 : 0;
      function run() {
        var vin = val(w, 'sar-v'); show(w, 'sar-v', f2(vin, 1) + ' V');
        var code = 0, rows = [], pts = [];
        for (var i = 0; i < Math.min(k, 4); i++) {
          var bit = 3 - i, trial = code | (1 << bit), keep = trial <= vin; rows.push('گام ' + (i + 1) + ': آزمون <b>' + ('000' + trial.toString(2)).slice(-4) + '</b> = ' + trial + 'V ' + (keep ? '≤' : '>') + ' ' + f2(vin, 1) + ' ⇒ بیت ' + bit + ' = ' + (keep ? 1 : 0));
          if (keep) code = trial; pts.push([i, trial], [i + 1, trial]);
        }
        $('.sv', w).innerHTML = plotSVG({ x: [0, 4], y: [0, 16], xt: [0, 1, 2, 3, 4], yt: [0, 4, 8, 12, 16], xl: 'گام', yl: 'D/A (V)', c: [{ f: String(vin), k: 2, d: 1, w: 1.6 }].concat(pts.length ? [{ p: pts, k: 1 }] : []) });
        $('.read', w).innerHTML = (rows.length ? rows.join('<br>') : 'روی «گام بعد» بزنید.') + (k >= 4 ? '<br>خروجی نهایی: <b>' + ('000' + code.toString(2)).slice(-4) + '</b> = ' + code + ' (کف ' + f2(vin, 1) + ')' : '');
      }
      $('#sar-v', w).addEventListener('input', function () { k = 0; run(); });
      $('#sar-step', w).addEventListener('click', function () { if (k < 4) k++; run(); });
      $('#sar-reset', w).addEventListener('click', function () { k = 0; run(); });
      run();
    },
    vtc: function (w) {
      w.innerHTML = '<div class="wt">منحنی انتقال معکوس‌کننده CMOS</div><p class="wd">VDD = 5V و Vtn = |Vtp| = 1V. نسبت قدرت دو ترانزیستور r = kn/kp را عوض کنید: وقتی NMOS قوی‌تر است، نقطه سوئیچ VM به چپ می‌رود و برعکس. منحنی از حل عددی «جریان NMOS = جریان PMOS» در هر ورودی به دست آمده است.</p>' +
        '<div class="ctrls">' + slider('vt-r', 'نسبت r = kn/kp', 0.25, 4, 0.05, 1) + '</div><div class="sv"></div><div class="read"></div>';
      bind(w, ['vt-r'], function () {
        var r = val(w, 'vt-r'), V = 5, Vt = 1; show(w, 'vt-r', f2(r));
        function In(vi, vo) { var ov = vi - Vt; if (ov <= 0) return 0; return vo >= ov ? r * ov * ov / 2 : r * (ov * vo - vo * vo / 2); }
        function Ip(vi, vo) { var ov = V - vi - Vt, sd = V - vo; if (ov <= 0) return 0; return sd >= ov ? ov * ov / 2 : (ov * sd - sd * sd / 2); }
        var pts = [];
        for (var i = 0; i <= 500; i++) { var vi = V * i / 500, lo = 0, hi = V; for (var j = 0; j < 50; j++) { var mid = (lo + hi) / 2; if (In(vi, mid) - Ip(vi, mid) > 0) hi = mid; else lo = mid; } pts.push([vi, (lo + hi) / 2]); }
        var sr = Math.sqrt(r), VM = (V - Vt + Vt * sr) / (1 + sr);
        $('.sv', w).innerHTML = plotSVG({ x: [0, 5], y: [0, 5], xt: [0, 1, 2, 3, 4, 5], yt: [0, 1, 2, 3, 4, 5], xl: 'Vin (V)', yl: 'Vout (V)', c: [{ p: pts, k: 1 }, { f: 'x', k: 6, d: 1, w: 1.2 }], vx: [VM], pts: [[VM, VM, 'VM', 'start']] });
        $('.read', w).innerHTML = 'VM = (VDD − |Vtp| + Vtn·√r)/(1 + √r) = <b>' + f2(VM) + ' V</b>' + (Math.abs(r - 1) < 0.03 ? ' <span class="mut">(متقارن: دقیقاً VDD/2)</span>' : '');
      });
    }
  };
  function initWidget(w) {
    if (w.dataset.done) return; w.dataset.done = '1';
    var f = WIDGETS[w.dataset.w];
    if (f) { try { f(w); } catch (e) { w.textContent = 'widget error: ' + e.message; } }
  }

  if (PRINT) {
    pages.forEach(function (p) { $$('figure.plot', p).forEach(drawPlotFigure); $$('.widget', p).forEach(initWidget); });
    $$('details').forEach(function (d) { d.open = true; });
  } else {
    route();
  }
})();
