from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, box, nfet, pfet, npass, INK
from schemdraw import logic


@ckt('c7-array')
def _():
    d = new(fontsize=12)
    box(d, -2.6, 0, -0.6, 5, 'رمزگشا', color=BL)
    wire(d, (-3.8, 2.5), (-2.6, 2.5)); text(d, -4.4, 2.9, 'آدرس')
    for k, y in enumerate((4.3, 3.2, 2.1, 1.0)):
        col = HL if k == 1 else MU
        wire(d, (-0.6, y), (7.2, y), color=col)
        text(d, 7.9, y, 'WL%d' % k + (' = 1' if k == 1 else ''), color=col)
        for x in (1.0, 2.8, 4.6, 6.4):
            dot(d, (x, y))
    for j, x in enumerate((1.0, 2.8, 4.6, 6.4)):
        wire(d, (x, 5.0), (x, -0.4))
        text(d, x, 5.4, 'BL%d' % j)
    box(d, 0.4, -1.6, 7.0, -0.4, 'تقویت‌کننده حس / داده', color=MU)
    return d


@ckt('c7-rom')
def _():
    d = new(fontsize=12)
    xs = (0, 3.2)
    for j, x in enumerate(xs):
        p = pfet(d, (x, 6.2), color=MU)
        wire(d, p.source, (x, 6.6)); text(d, x, 7.0, 'V_DD')
        wire(d, p.gate, (p.gate[0] - 0.5, p.gate[1])); gnd(d, (p.gate[0] - 0.5, p.gate[1]))
        wire(d, p.drain, (x, 0))
        text(d, x + 0.5, -0.4, 'BL%d' % j)
    # word lines
    for k, y in enumerate((3.6, 1.6)):
        wire(d, (-2.6, y), (4.8, y), color=BL)
        text(d, -3.1, y, 'WL%d' % k, color=BL)
    # transistors at (WL0,BL0) and (WL1,BL1)
    for (x, yw) in ((0, 3.6), (3.2, 1.6)):
        q = nfet(d, (x + 1.2, yw - 1.2), color=HL)
        wire(d, q.drain, (x + 1.2, yw - 0.1 + 0.0))
        wire(d, (x + 1.2, q.drain[1]), (x + 1.2, q.drain[1] + 0.2), (x, q.drain[1] + 0.2))
        dot(d, (x, q.drain[1] + 0.2))
        wire(d, q.gate, (q.gate[0], yw))
        dot(d, (q.gate[0], yw), )
        gnd(d, q.source)
    return d


@ckt('c7-dram')
def _():
    d = new(fontsize=12)
    wire(d, (0, 5), (0, -0.5)); text(d, 0, 5.4, 'BL')
    el(d, E.Capacitor, (-1.6, 2.8), (-1.6, 0.8), 'C_BL', loc='top', color=MU)
    wire(d, (-1.6, 2.8), (0, 2.8)); dot(d, (0, 2.8)); gnd(d, (-1.6, 0.8))
    q = npass(d, (0, 3.8), color=HL)
    wire(d, (1.5, 3.8), (2.4, 3.8))
    el(d, E.Capacitor, (2.4, 3.8), (2.4, 1.8), 'C_s', loc='bottom', color=HL)
    gnd(d, (2.4, 1.8))
    wire(d, q.gate, (q.gate[0], 5.2), (3.6, 5.2)); text(d, 4.0, 5.2, 'WL', color=BL)
    dot(d, (0, 3.8))
    return d


@ckt('c7-sram')
def _():
    d = new(fontsize=12)
    a = logic.Not().at((2.0, 3.4)).right(); d += a
    b = logic.Not().at((a.out[0], 1.8)).left(); d += b
    xl = b.out[0] - 0.5; xr = a.out[0] + 0.5
    wire(d, a.out, (xr, a.out[1]), (xr, b.in1[1]), b.in1)
    wire(d, b.out, (xl, b.out[1]), (xl, a.in1[1]), a.in1)
    nl = (xl, 2.6); nr = (xr, 2.6)
    dot(d, nl, nr)
    text(d, xl + 0.4, 2.6, 'D')
    text(d, xr - 0.4, 2.6, 'D̅')
    # access transistors
    ql = npass(d, (xl - 1.9, 2.6), color=HL)
    wire(d, (xl - 0.4, 2.6), nl)
    qr = npass(d, (xr + 0.4, 2.6), color=HL)
    wire(d, nr, (xr + 0.4, 2.6))
    wire(d, (xl - 1.9, 2.6), (xl - 2.4, 2.6)); wire(d, (xl - 2.4, 5.6), (xl - 2.4, -0.4)); dot(d, (xl - 2.4, 2.6))
    wire(d, (xr + 1.9, 2.6), (xr + 2.4, 2.6)); wire(d, (xr + 2.4, 5.6), (xr + 2.4, -0.4)); dot(d, (xr + 2.4, 2.6))
    text(d, xl - 2.4, 6.0, 'BL'); text(d, xr + 2.4, 6.0, 'BL̅')
    wire(d, ql.gate, (ql.gate[0], 4.8), (qr.gate[0], 4.8), qr.gate, color=BL)
    text(d, (ql.gate[0] + qr.gate[0]) / 2, 5.15, 'WL', color=BL)
    return d
