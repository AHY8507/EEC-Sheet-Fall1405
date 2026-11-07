from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, box, INK
from schemdraw import logic


def opamp(d, at=(0, 0)):
    op = E.Opamp(leads=True).at(at).anchor('center').right()
    d += op
    return op


@ckt('c8-osc')
def _():
    d = new(fontsize=12)
    i1 = logic.Not().at((1.2, 2)).right(); d += i1
    i2 = logic.Not().at((i1.out[0] + 1.6, 2)).right(); d += i2
    wire(d, i1.out, (i1.out[0] + 1.6, 2))
    A = (i1.out[0] + 0.8, 2); dot(d, A); text(d, A[0], 2.45, 'A')
    Bp = (i2.out[0] + 0.6, 2); wire(d, i2.out, Bp); dot(d, Bp); text(d, Bp[0] + 0.4, 2.45, 'B')
    Cn = (0.4, 2); wire(d, Cn, i1.in1); dot(d, Cn); text(d, Cn[0] - 0.4, 2.45, 'X')
    el(d, E.Resistor, A, (A[0], 0.2), 'R', loc='bottom', color=BL)
    wire(d, (A[0], 0.2), (0.4, 0.2), Cn)
    el(d, E.Capacitor, Bp, (Bp[0], 4.0), 'C', loc='bottom', color=HL)
    wire(d, (Bp[0], 4.0), (0.4, 4.0), Cn)
    return d


@ckt('c8-wdac')
def _():
    d = new(fontsize=12)
    op = opamp(d, (6, 0))
    wire(d, op.in2, (op.in2[0], op.in2[1] - 0.6)); gnd(d, (op.in2[0], op.in2[1] - 0.6))
    n = (op.in1[0] - 0.6, op.in1[1]); wire(d, n, op.in1); dot(d, n)
    labs = [('b₃', 'R'), ('b₂', '2R'), ('b₁', '4R'), ('b₀', '8R')]
    for k, (b, r) in enumerate(labs):
        y = n[1] + 2.4 - k * 1.3
        el(d, E.Resistor, (n[0] - 3.0, y), (n[0] - 0.6, y), r)
        wire(d, (n[0] - 0.6, y), (n[0], y))
        el(d, E.Switch, (n[0] - 4.6, y), (n[0] - 3.0, y), '', action='close')
        text(d, n[0] - 5.0, y, b, color=HL)
    wire(d, (n[0], n[1] + 2.4), (n[0], n[1] - 1.5))
    wire(d, (n[0], n[1] + 2.4), (n[0], n[1] + 3.4))
    el(d, E.Resistor, (n[0], n[1] + 3.4), (op.out[0], n[1] + 3.4), 'R_f', color=BL)
    wire(d, (op.out[0], n[1] + 3.4), op.out)
    wire(d, op.out, (op.out[0] + 1.0, op.out[1])); dot(d, (op.out[0] + 1.0, op.out[1]), open=True, lab='V_out', loc='right')
    text(d, n[0] - 4.0, n[1] + 3.4, 'هر کلید: V_ref (بیت ۱) یا زمین (بیت ۰)')
    return d


@ckt('c8-r2r')
def _():
    d = new(fontsize=12)
    xs = [0, 2.6, 5.2]
    el(d, E.Resistor, (-2.6, 3), (0, 3), '2R')
    gnd(d, (-2.6, 3)) if False else None
    wire(d, (-2.6, 3), (-2.6, 2.6)); gnd(d, (-2.6, 2.6))
    for k, x in enumerate(xs):
        dot(d, (x, 3))
        el(d, E.Resistor, (x, 3), (x, 0.6), '2R', loc='bottom')
        text(d, x, 0.1, 'a%d' % k, color=HL)
        if k < 2:
            el(d, E.Resistor, (x, 3), (xs[k + 1], 3), 'R')
    op = opamp(d, (11, 2.2))
    el(d, E.Resistor, (5.2, 3), (op.in1[0] - 0.3, 3), '2R')
    wire(d, (op.in1[0] - 0.3, 3), (op.in1[0] - 0.3, op.in1[1]), op.in1)
    wire(d, op.in2, (op.in2[0], op.in2[1] - 0.6)); gnd(d, (op.in2[0], op.in2[1] - 0.6))
    dot(d, (op.in1[0] - 0.3, op.in1[1]))
    wire(d, (op.in1[0] - 0.3, op.in1[1]), (op.in1[0] - 0.3, op.in1[1] + 2.0))
    el(d, E.Resistor, (op.in1[0] - 0.3, op.in1[1] + 2.0), (op.out[0], op.in1[1] + 2.0), '3R', color=BL)
    wire(d, (op.out[0], op.in1[1] + 2.0), op.out)
    dot(d, (op.out[0] + 0.9, op.out[1]), open=True, lab='V_o', loc='right'); wire(d, op.out, (op.out[0] + 0.9, op.out[1]))
    text(d, 2.6, -0.6, 'هر a_i: V_ref یا زمین')
    return d


@ckt('c8-flash')
def _():
    d = new(fontsize=12)
    text(d, 0, 7.6, 'V_ref = 5V')
    ys = [6.0, 4.5, 3.0, 1.5]
    lv = ['4V', '3V', '2V', '1V']
    el(d, E.Resistor, (0, 7.2), (0, 6.0), 'R', loc='top')
    for k in range(3):
        el(d, E.Resistor, (0, ys[k]), (0, ys[k + 1]), 'R', loc='top')
    el(d, E.Resistor, (0, 1.5), (0, 0.0), 'R', loc='top'); gnd(d, (0, 0))
    for k, y in enumerate(ys):
        dot(d, (0, y))
        op = E.Opamp(leads=False).at((2.8, y)).anchor('in1').right().scale(0.55)
        d += op
        wire(d, (0, y), op.in1)
        text(d, 0.9, y + 0.35, lv[k], color=MU)
        wire(d, op.in2, (1.8, op.in2[1]))
        wire(d, op.out, (5.8, op.out[1]))
        text(d, 5.25, op.out[1] + 0.3, 'a%d' % (3 - k), color=HL)
    wire(d, (1.8, ys[0] - 0.55), (1.8, -0.8), (-1.4, -0.8))
    text(d, -2.4, -0.8, 'V_in (از S/H)')
    box(d, 5.8, 0.8, 8.4, 6.6, 'رمزگذار اولویت‌دار', color=BL)
    for k, y in enumerate((5.0, 3.7, 2.4)):
        wire(d, (8.4, y), (9.4, y)); text(d, 9.8, y, 'b%d' % (2 - k))
    return d


@ckt('c8-sar')
def _():
    d = new(fontsize=12)
    box(d, 0, 0, 2.6, 1.6, 'S/H', color=MU)
    op = E.Opamp(leads=True).at((4.4, 0.8)).anchor('in1').right().scale(0.8); d += op
    wire(d, (2.6, 0.8), (op.in1[0], op.in1[1]))
    box(d, 7.2, -0.2, 10.0, 1.8, 'ثبات SAR', color=HL)
    wire(d, op.out, (7.2, op.out[1]))
    box(d, 7.2, -3.0, 10.0, -1.4, 'D/A', color=BL)
    wire(d, (8.6, -0.2), (8.6, -1.4))
    wire(d, (7.2, -2.2), (op.in2[0] - 0.4, -2.2), (op.in2[0] - 0.4, op.in2[1]), op.in2)
    wire(d, (10.0, 0.8), (11.2, 0.8)); text(d, 12.4, 0.8, 'خروجی n بیتی')
    wire(d, (-1.2, 0.8), (0, 0.8)); text(d, -2.0, 0.8, 'V_in')
    text(d, 8.6, 2.3, 'CLK')
    return d
