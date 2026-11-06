"""Circuit-drawing helpers on top of schemdraw.

Every circuit is a function registered with @ckt('name') that returns a schemdraw Drawing.
The build turns it into an inline SVG whose colors follow the page theme (CSS variables).
"""
import re
import schemdraw
import schemdraw.elements as elm
from schemdraw import logic  # noqa: F401  (used by circuit modules)

schemdraw.use('svg')

INK = '#010101'   # -> var(--ink)
HL = '#c00001'    # -> var(--copper)   highlight
BL = '#0000fe'    # -> var(--c-def)    second highlight
GR = '#00a001'    # -> var(--c-ex)
MU = '#808081'    # -> var(--ink-3)    muted

REG = {}


def ckt(name):
    def deco(fn):
        if name in REG:
            raise ValueError('duplicate circuit name: ' + name)
        REG[name] = fn
        return fn
    return deco


def new(unit=2.6, fontsize=13, lw=1.5):
    d = schemdraw.Drawing(show=False)
    d.config(unit=unit, fontsize=fontsize, color=INK, font='sans-serif', lw=lw)
    return d


def to_svg(d, scale=1.3):
    s = d.get_imagedata('svg')
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    for a, b in ((INK, 'var(--ink)'), (HL, 'var(--copper)'), (BL, 'var(--c-def)'), (GR, 'var(--c-ex)'), (MU, 'var(--ink-3)')):
        s = s.replace(a, b)
    s = s.replace('stroke-dasharray:-;', '')
    m = re.search(r'width="([\d.]+)pt"', s)
    w = float(m.group(1)) * scale if m else 360
    s = re.sub(r'\s(height|width)="[\d.]+pt"', '', s, count=2)
    s = s.replace('<svg ', '<svg style="width:%dpx" role="img" ' % round(w), 1)
    s = re.sub(r'<\?xml[^>]*>', '', s)
    return s.strip()


# short aliases used in circuit modules
E = elm


def box(d, x1, y1, x2, y2, text='', color=None):
    """A labelled rectangle (e.g. 'rest of the circuit')."""
    for a, b in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        ln = E.Line().at(a).to(b)
        if color:
            ln = ln.color(color)
        d += ln
    if text:
        d += E.Label().at(((x1 + x2) / 2, (y1 + y2) / 2)).label(text)
    return d


def text(d, x, y, s, **kw):
    d += E.Label().at((x, y)).label(s, **kw)
    return d


def el(d, kind, p1, p2, lab=None, loc=None, color=None, **kw):
    """Place a two-terminal element between two points."""
    e = kind(**kw).endpoints(p1, p2)
    if lab is not None:
        e = e.label(lab, loc=loc) if loc else e.label(lab)
    if color:
        e = e.color(color)
    d += e
    return e


def wire(d, *pts, color=None):
    for a, b in zip(pts, pts[1:]):
        ln = E.Line().at(a).to(b)
        if color:
            ln = ln.color(color)
        d += ln


def dot(d, *pts, open=False, lab=None, loc='top'):
    for p in pts:
        x = E.Dot(open=open).at(p)
        if lab:
            x = x.label(lab, loc=loc)
        d += x


def gnd(d, p):
    d += E.Ground().at(p)


def arrow(d, p1, p2, lab=None, color=None):
    a = E.Arrow().at(p1).to(p2)
    if lab:
        a = a.label(lab)
    if color:
        a = a.color(color)
    d += a
