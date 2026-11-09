from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, nfet, pfet, box


def gate_in(d, q, name, color=None):
    wire(d, q.gate, (q.gate[0] - 0.7, q.gate[1]), color=color)
    text(d, q.gate[0] - 1.05, q.gate[1], name, color=color or '#010101')


@ckt('c5-structure')
def _():
    d = new(fontsize=12)
    wire(d, (0, 6), (4, 6)); text(d, 2, 6.4, 'V_DD')
    wire(d, (2, 6), (2, 5.4))
    box(d, 0.6, 3.8, 3.4, 5.4, 'بالاکش (PMOS)', color=HL)
    wire(d, (2, 3.8), (2, 2.6))
    dot(d, (2, 3.2)); wire(d, (2, 3.2), (4.6, 3.2)); dot(d, (4.6, 3.2), open=True, lab='F', loc='right')
    box(d, 0.6, 1.0, 3.4, 2.6, 'پایین‌کش (NMOS)', color=BL)
    wire(d, (2, 1.0), (2, 0.4)); gnd(d, (2, 0.4))
    wire(d, (-1.4, 4.6), (0.6, 4.6)); wire(d, (-1.4, 1.8), (0.6, 1.8))
    text(d, -1.9, 3.2, 'ورودی‌ها')
    wire(d, (-1.4, 4.6), (-1.4, 1.8))
    return d


@ckt('c5-nand2')
def _():
    d = new(fontsize=12)
    wire(d, (-0.3, 6.2), (3.0, 6.2)); text(d, 1.35, 6.6, 'V_DD')
    pa = pfet(d, (0, 6.2), color=HL); gate_in(d, pa, 'A', HL)
    pb = pfet(d, (2.7, 6.2), color=HL); gate_in(d, pb, 'B', HL)
    wire(d, pa.drain, (pb.drain[0], pa.drain[1]))
    out = (pb.drain[0], pb.drain[1])
    na = nfet(d, (2.7, 2.6), color=BL); gate_in(d, na, 'A', BL)
    wire(d, out, na.drain)
    nb = nfet(d, (2.7, 1.1), color=BL); gate_in(d, nb, 'B', BL)
    gnd(d, nb.source)
    dot(d, out)
    wire(d, (out[0], out[1] - 0.45), (out[0] + 1.4, out[1] - 0.45)); dot(d, (out[0], out[1] - 0.45))
    dot(d, (out[0] + 1.4, out[1] - 0.45), open=True, lab='F = (AB)′', loc='right')
    return d


@ckt('c5-nor2')
def _():
    d = new(fontsize=12)
    wire(d, (2.7, 7.6), (2.7, 7.9)); text(d, 2.7, 8.3, 'V_DD')
    pa = pfet(d, (2.7, 7.6), color=HL); gate_in(d, pa, 'A', HL)
    pb = pfet(d, (2.7, 6.1), color=HL); gate_in(d, pb, 'B', HL)
    out = pb.drain
    wire(d, out, (out[0], 3.8))
    na = nfet(d, (0, 2.3), color=BL); gate_in(d, na, 'A', BL)
    nb = nfet(d, (2.7, 2.3), color=BL); gate_in(d, nb, 'B', BL)
    wire(d, na.drain, (2.7, na.drain[1]))
    wire(d, (0, 2.3), (2.7, 2.3)); gnd(d, (1.35, 2.3))
    dot(d, (2.7, 3.8))
    wire(d, (2.7, 4.3), (4.1, 4.3)); dot(d, (2.7, 4.3))
    dot(d, (4.1, 4.3), open=True, lab='F = (A+B)′', loc='right')
    return d


@ckt('c5-cx')
def _():
    d = new(fontsize=12)
    # pull-up: A parallel with (B series C)
    wire(d, (-0.3, 8.0), (3.0, 8.0)); text(d, 1.35, 8.4, 'V_DD')
    pa = pfet(d, (0, 8.0), color=HL); gate_in(d, pa, 'A', HL)
    pb = pfet(d, (2.7, 8.0), color=HL); gate_in(d, pb, 'B', HL)
    pc = pfet(d, (2.7, 6.5), color=HL); gate_in(d, pc, 'C', HL)
    wire(d, pa.drain, (0, pc.drain[1]), (2.7, pc.drain[1]))
    out = pc.drain
    dot(d, out)
    # pull-down: A series (B parallel C)
    na = nfet(d, (2.7, 2.9), color=BL); gate_in(d, na, 'A', BL)
    wire(d, out, na.drain)
    nb = nfet(d, (2.7, 1.4), color=BL); gate_in(d, nb, 'B', BL)
    nc = nfet(d, (5.0, 1.4), color=BL)
    wire(d, nc.gate, (nc.gate[0] - 0.35, nc.gate[1])); text(d, nc.gate[0] - 0.35, nc.gate[1] + 0.4, 'C', color=BL)
    wire(d, (2.7, 2.9), (5.0, 2.9))
    wire(d, (2.7, 1.4), (5.0, 1.4)); gnd(d, (3.85, 1.4))
    dot(d, (2.7, 2.9))
    wire(d, (2.7, 4.2), (6.4, 4.2)); dot(d, (2.7, 4.2))
    dot(d, (6.4, 4.2), open=True, lab='F = (A(B+C))′', loc='right')
    return d


@ckt('c5-dyn')
def _():
    d = new(fontsize=12)
    wire(d, (0, 6.4), (0, 6.7)); text(d, 0, 7.1, 'V_DD')
    p = pfet(d, (0, 6.4), color=HL); gate_in(d, p, 'φ', HL)
    out = p.drain
    dot(d, out)
    wire(d, out, (2.0, out[1])); el(d, E.Capacitor, (2.0, out[1]), (2.0, out[1] - 1.6), 'C_L', loc='bottom', color=MU); gnd(d, (2.0, out[1] - 1.6))
    wire(d, out, (0, 4.3))
    box(d, -1.1, 2.3, 1.1, 4.3, 'شبکه NMOS', color=BL)
    text(d, -1.9, 3.3, 'ورودی‌ها')
    wire(d, (0, 2.3), (0, 1.9))
    n = nfet(d, (0, 0.4), color=HL); gate_in(d, n, 'φ', HL)
    gnd(d, n.source)
    wire(d, out, (out[0] + 3.4, out[1]))
    dot(d, (out[0] + 3.4, out[1]), open=True, lab='out', loc='right')
    return d
