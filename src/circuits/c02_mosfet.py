from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


def nfet(d, at, color=None, lab=None):
    q = E.NFet(bulk=False).at(at).anchor('source').right().reverse()
    if color:
        q = q.color(color)
    if lab:
        q = q.label(lab, loc='right')
    d += q
    return q


def pfet(d, at, color=None, lab=None):
    q = E.PFet(bulk=False).at(at).anchor('source').right().reverse()
    if color:
        q = q.color(color)
    if lab:
        q = q.label(lab, loc='right')
    d += q
    return q


@ckt('c2-sym')
def _():
    d = new(fontsize=12)
    q = nfet(d, (0, 0))
    text(d, q.drain[0] + 0.5, q.drain[1], 'D', loc='right')
    text(d, q.source[0] + 0.5, q.source[1], 'S', loc='right')
    text(d, q.gate[0] - 0.4, q.gate[1] + 0.35, 'G')
    text(d, q.center[0], q.source[1] - 1.0, 'NMOS')
    d += E.Arrow().at((q.drain[0] + 1.3, q.drain[1] - 0.2)).to((q.source[0] + 1.3, q.source[1] + 0.2)).label('I_DS', loc='right')
    p = pfet(d, (6, 1.5))
    text(d, p.source[0] + 0.5, p.source[1], 'S', loc='right')
    text(d, p.drain[0] + 0.5, p.drain[1], 'D', loc='right')
    text(d, p.gate[0] - 0.4, p.gate[1] + 0.35, 'G')
    text(d, p.center[0], p.drain[1] - 1.0, 'PMOS')
    d += E.Arrow().at((p.source[0] + 1.3, p.source[1] - 0.2)).to((p.drain[0] + 1.3, p.drain[1] + 0.2)).label('I_SD', loc='right')
    return d


@ckt('c2-bias')
def _():
    d = new()
    q = nfet(d, (0, 0), color=HL)
    gnd(d, q.source)
    el(d, E.Resistor, q.drain, (q.drain[0], q.drain[1] + 2.5), 'R_D', loc='bottom')
    text(d, q.drain[0], q.drain[1] + 3.0, 'V_DD = 5V')
    wire(d, q.gate, (q.gate[0] - 1.5, q.gate[1]))
    dot(d, (q.gate[0] - 1.5, q.gate[1]), open=True, lab='V_G = 1.8V', loc='left')
    dot(d, q.drain)
    wire(d, q.drain, (q.drain[0] + 1.5, q.drain[1]))
    dot(d, (q.drain[0] + 1.5, q.drain[1]), open=True, lab='V_D', loc='right')
    return d


@ckt('c2-degen')
def _():
    d = new()
    q = nfet(d, (0, 0), color=HL)
    el(d, E.Resistor, q.source, (q.source[0], q.source[1] - 2.2), 'R_S = 1k', loc='bottom')
    gnd(d, (q.source[0], q.source[1] - 2.2))
    el(d, E.Resistor, q.drain, (q.drain[0], q.drain[1] + 2.5), 'R_D = 2k', loc='bottom')
    text(d, q.drain[0], q.drain[1] + 3.0, 'V_DD = 5V')
    wire(d, q.gate, (q.gate[0] - 1.5, q.gate[1]))
    dot(d, (q.gate[0] - 1.5, q.gate[1]), open=True, lab='V_G = 3V', loc='left')
    dot(d, q.source)
    return d


@ckt('c2-pmos')
def _():
    d = new()
    q = pfet(d, (0, 1.5), color=HL)
    wire(d, q.source, (q.source[0], q.source[1] + 0.8))
    text(d, q.source[0], q.source[1] + 1.3, 'V_DD = 3V')
    el(d, E.Resistor, q.drain, (q.drain[0], q.drain[1] - 2.5), 'R_D = 2k', loc='bottom')
    gnd(d, (q.drain[0], q.drain[1] - 2.5))
    wire(d, q.gate, (q.gate[0] - 1.5, q.gate[1]))
    dot(d, (q.gate[0] - 1.5, q.gate[1]), open=True, lab='V_G = 1V', loc='left')
    dot(d, q.drain)
    return d


@ckt('c2-diodecon')
def _():
    d = new()
    q = nfet(d, (0, 0), color=HL)
    gnd(d, q.source)
    wire(d, q.drain, (q.drain[0], q.drain[1] + 0.8), (q.gate[0] - 0.8, q.drain[1] + 0.8), (q.gate[0] - 0.8, q.gate[1]), q.gate)
    dot(d, (q.drain[0], q.drain[1] + 0.8))
    el(d, E.SourceI, (q.drain[0], q.drain[1] + 3.2), (q.drain[0], q.drain[1] + 0.8), 'I = 1mA', loc='bottom')
    return d
