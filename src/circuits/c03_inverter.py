from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, nfet, pfet


@ckt('c3-res')
def _():
    d = new()
    q = nfet(d, (0, 0), color=HL)
    gnd(d, q.source)
    el(d, E.Resistor, q.drain, (q.drain[0], q.drain[1] + 2.5), 'R', loc='bottom')
    text(d, q.drain[0], q.drain[1] + 3.0, 'V_DD')
    wire(d, q.gate, (q.gate[0] - 1.4, q.gate[1]))
    dot(d, (q.gate[0] - 1.4, q.gate[1]), open=True, lab='V_I', loc='left')
    dot(d, q.drain)
    wire(d, q.drain, (q.drain[0] + 1.5, q.drain[1]))
    dot(d, (q.drain[0] + 1.5, q.drain[1]), open=True, lab='V_out', loc='right')
    return d


@ckt('c3-q2')
def _():
    d = new()
    q1 = nfet(d, (0, 0), color=HL, lab='Q₁')
    gnd(d, q1.source)
    q2 = nfet(d, q1.drain, lab='Q₂')
    wire(d, q2.drain, (q2.drain[0], q2.drain[1] + 0.7))
    text(d, q2.drain[0], q2.drain[1] + 1.2, 'V_DD')
    wire(d, q2.gate, (q2.gate[0] - 0.6, q2.gate[1]), (q2.gate[0] - 0.6, q2.drain[1] + 0.4), (q2.drain[0], q2.drain[1] + 0.4))
    dot(d, (q2.drain[0], q2.drain[1] + 0.4))
    wire(d, q1.gate, (q1.gate[0] - 1.4, q1.gate[1]))
    dot(d, (q1.gate[0] - 1.4, q1.gate[1]), open=True, lab='V_I', loc='left')
    dot(d, q1.drain)
    wire(d, q1.drain, (q1.drain[0] + 1.5, q1.drain[1]))
    dot(d, (q1.drain[0] + 1.5, q1.drain[1]), open=True, lab='V_out', loc='right')
    return d


@ckt('c3-cmos')
def _():
    d = new()
    qn = nfet(d, (0, 0), color=BL, lab='Q_n')
    gnd(d, qn.source)
    qp = pfet(d, (0, 4.2), color=HL, lab='Q_p')
    wire(d, qp.drain, qn.drain)
    wire(d, qp.source, (0, 4.8))
    text(d, 0, 5.2, 'V_DD')
    x = qn.gate[0] - 0.8
    wire(d, qn.gate, (x, qn.gate[1]), (x, qp.gate[1]), qp.gate)
    m = (x, (qn.gate[1] + qp.gate[1]) / 2)
    dot(d, m)
    wire(d, m, (x - 1.2, m[1]))
    dot(d, (x - 1.2, m[1]), open=True, lab='V_in', loc='left')
    mid = ((qn.drain[0]), (qn.drain[1] + qp.drain[1]) / 2)
    dot(d, mid)
    wire(d, mid, (mid[0] + 2.0, mid[1]))
    dot(d, (mid[0] + 2.0, mid[1]), open=True, lab='V_out', loc='right')
    return d


@ckt('c3-switch')
def _():
    d = new(fontsize=12)
    # charging
    text(d, 0, 4.1, 'V_DD')
    wire(d, (0, 3.7), (0, 3.4))
    el(d, E.Resistor, (0, 3.4), (0, 1.6), 'R_on,p', loc='bottom', color=HL)
    wire(d, (0, 1.6), (0, 1.3), (1.6, 1.3))
    el(d, E.Capacitor, (1.6, 1.3), (1.6, -0.6), 'C', loc='bottom')
    gnd(d, (1.6, -0.6))
    d += E.Arrow().at((-0.6, 3.0)).to((-0.6, 2.0)).color(HL)
    text(d, 0.8, -1.4, 'شارژ: Q_p روشن')
    o = 6
    wire(d, (o, 1.3), (o + 1.6, 1.3))
    el(d, E.Capacitor, (o, 1.3), (o, -0.6), 'C', loc='top')
    gnd(d, (o, -0.6))
    el(d, E.Resistor, (o + 1.6, 1.3), (o + 1.6, -0.6), 'R_on,n', loc='bottom', color=BL)
    gnd(d, (o + 1.6, -0.6))
    text(d, o + 0.8, -1.4, 'دشارژ: Q_n روشن')
    return d
