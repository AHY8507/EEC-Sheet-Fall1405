from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, box, tg, nfet, pfet, INK
from schemdraw import logic


@ckt('c6-xinv')
def _():
    d = new(fontsize=12)
    a = logic.Not().at((0, 2)).right()
    d += a
    b = logic.Not().at((a.out[0] + 0.0, 0)).left()
    d += b
    wire(d, a.out, (a.out[0] + 0.6, a.out[1]), (a.out[0] + 0.6, b.in1[1]), b.in1)
    wire(d, b.out, (b.out[0] - 0.6, b.out[1]), (b.out[0] - 0.6, a.in1[1]), a.in1)
    dot(d, (a.out[0] + 0.6, a.out[1]), (b.out[0] - 0.6, a.in1[1]))
    text(d, a.out[0] + 1.1, a.out[1] + 0.2, 'Q')
    text(d, b.out[0] - 1.1, a.in1[1] + 0.2, 'Q̅')
    return d


@ckt('c6-sr')
def _():
    d = new(fontsize=12)
    g1 = logic.Nor().at((0, 3)).right().anchor('in1')
    d += g1
    g2 = logic.Nor().at((0, 0)).right().anchor('in2')
    d += g2
    wire(d, g1.in1, (g1.in1[0] - 1, g1.in1[1])); text(d, g1.in1[0] - 1.4, g1.in1[1], 'S')
    wire(d, g2.in2, (g2.in2[0] - 1, g2.in2[1])); text(d, g2.in2[0] - 1.4, g2.in2[1], 'R')
    x1 = g1.out[0] + 0.5
    wire(d, g1.out, (x1 + 1.2, g1.out[1])); text(d, x1 + 1.6, g1.out[1], 'Q̅')
    wire(d, g2.out, (x1 + 1.2, g2.out[1])); text(d, x1 + 1.6, g2.out[1], 'Q')
    dot(d, (x1, g1.out[1]), (x1, g2.out[1]))
    wire(d, (x1, g1.out[1]), (x1, g1.out[1] - 0.9), (g2.in1[0] - 0.4, g2.in1[1] + 0.9), (g2.in1[0] - 0.4, g2.in1[1]), g2.in1)
    wire(d, (x1, g2.out[1]), (x1, g2.out[1] + 0.9), (g1.in2[0] - 0.4, g1.in2[1] - 0.9), (g1.in2[0] - 0.4, g1.in2[1]), g1.in2)
    return d


@ckt('c6-tglatch')
def _():
    d = new(fontsize=12)
    dot(d, (0, 2), open=True, lab='D', loc='left')
    tg(d, (0, 2), 'CLK', color=HL)
    wire(d, (2.5, 2), (3.2, 2)); dot(d, (3.2, 2)); text(d, 3.2, 2.45, 'X')
    i1 = logic.Not().at((3.2, 2)).right()
    d += i1
    i2 = logic.Not().at(i1.out).right()
    d += i2
    wire(d, i2.out, (i2.out[0] + 1.5, 2)); dot(d, (i2.out[0] + 0.6, 2))
    dot(d, (i2.out[0] + 1.5, 2), open=True, lab='Q', loc='right')
    xq = i2.out[0] + 0.6
    wire(d, (xq, 2), (xq, -1.8), (6.0, -1.8))
    tg(d, (3.5, -1.8), 'CLK̅', color=BL)
    wire(d, (3.5, -1.8), (3.2, -1.8), (3.2, 2))
    return d


@ckt('c6-c2mos')
def _():
    d = new(fontsize=12)
    wire(d, (0, 7.2), (0, 7.5)); text(d, 0, 7.9, 'V_DD')
    p1 = pfet(d, (0, 7.2))
    p2 = pfet(d, (0, 5.7), color=HL)
    n2 = nfet(d, (0, 2.6), color=HL)
    n1 = nfet(d, (0, 1.1))
    gnd(d, n1.source)
    wire(d, p2.drain, n2.drain)
    out = (0, (p2.drain[1] + n2.drain[1]) / 2)
    dot(d, out); wire(d, out, (1.6, out[1])); dot(d, (1.6, out[1]), open=True, lab='out', loc='right')
    xi = p1.gate[0] - 0.9
    wire(d, p1.gate, (xi, p1.gate[1]), (xi, n1.gate[1]), n1.gate)
    dot(d, (xi, (p1.gate[1] + n1.gate[1]) / 2))
    wire(d, (xi, (p1.gate[1] + n1.gate[1]) / 2), (xi - 0.9, (p1.gate[1] + n1.gate[1]) / 2))
    dot(d, (xi - 0.9, (p1.gate[1] + n1.gate[1]) / 2), open=True, lab='in', loc='left')
    wire(d, p2.gate, (p2.gate[0] - 0.5, p2.gate[1])); text(d, p2.gate[0] - 0.95, p2.gate[1] + 0.35, 'CLK̅', color=HL)
    wire(d, n2.gate, (n2.gate[0] - 0.5, n2.gate[1])); text(d, n2.gate[0] - 0.95, n2.gate[1] + 0.35, 'CLK', color=HL)
    return d


@ckt('c6-ms')
def _():
    d = new(fontsize=12)
    box(d, 0, 0, 2.6, 2.4, 'لچ D (Master)', color=BL)
    box(d, 4.4, 0, 7.0, 2.4, 'لچ D (Slave)', color=HL)
    wire(d, (-1.2, 1.7), (0, 1.7)); text(d, -1.6, 1.7, 'D')
    wire(d, (2.6, 1.7), (4.4, 1.7)); text(d, 3.5, 2.1, 'Q_m')
    wire(d, (7.0, 1.7), (8.2, 1.7)); text(d, 8.6, 1.7, 'Q')
    wire(d, (-1.2, 0.6), (0, 0.6)); text(d, -1.7, 0.6, 'CLK̅', color=BL)
    wire(d, (3.4, 0.6), (4.4, 0.6)); text(d, 3.0, 0.6, 'CLK', color=HL)
    return d


@ckt('c6-xwrite')
def _():
    d = new(fontsize=12)
    a = logic.Not().at((0, 4.2)).right(); d += a
    b = logic.Not().at((a.out[0], 2.4)).left(); d += b
    wire(d, a.out, (a.out[0] + 0.5, a.out[1]), (a.out[0] + 0.5, b.in1[1]), b.in1)
    wire(d, b.out, (b.out[0] - 0.5, b.out[1]), (b.out[0] - 0.5, a.in1[1]), a.in1)
    qb = (b.out[0] - 0.5, 3.3); q = (a.out[0] + 0.5, 3.3)
    text(d, qb[0] - 0.5, qb[1] + 0.6, 'Q̅'); text(d, q[0] + 0.5, q[1] + 0.6, 'Q')
    # write transistors
    n1 = nfet(d, (qb[0], 0.4), color=HL); wire(d, n1.drain, (qb[0], 2.4)); dot(d, (qb[0], 2.4))
    wire(d, n1.gate, (n1.gate[0] - 0.5, n1.gate[1])); text(d, n1.gate[0] - 0.9, n1.gate[1], 'D', color=HL)
    n2 = nfet(d, (q[0], 0.4), color=HL); wire(d, n2.drain, (q[0], 2.4)); dot(d, (q[0], 2.4))
    wire(d, n2.gate, (n2.gate[0] - 0.5, n2.gate[1])); text(d, n2.gate[0] - 0.9, n2.gate[1], 'D̅', color=HL)
    wire(d, (qb[0], 0.4), (q[0], 0.4))
    nc = nfet(d, ((qb[0] + q[0]) / 2, -1.1), color=BL); wire(d, nc.drain, ((qb[0] + q[0]) / 2, 0.4))
    dot(d, ((qb[0] + q[0]) / 2, 0.4))
    wire(d, nc.gate, (nc.gate[0] - 0.5, nc.gate[1])); text(d, nc.gate[0] - 1.0, nc.gate[1], 'CLK', color=BL)
    gnd(d, nc.source)
    return d
