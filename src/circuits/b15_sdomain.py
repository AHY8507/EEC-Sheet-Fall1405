from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('b15-cmodel')
def _():
    d = new(fontsize=12)
    dot(d, (0, 3.6), open=True, lab='+', loc='left')
    dot(d, (0, -1.0), open=True, lab='−', loc='left')
    el(d, E.Resistor, (0, 3.6), (0, 1.3), '1/sC', loc='bottom')
    el(d, E.SourceV, (0, -1.0), (0, 1.3), 'v(0⁻)/s', loc='bottom', color=HL)
    text(d, 0, -2.0, 'منبع ولتاژ سری')
    o = 5
    dot(d, (o, 3.6), open=True, lab='+', loc='left')
    dot(d, (o, -1.0), open=True, lab='−', loc='left')
    wire(d, (o, 3.6), (o + 2.5, 3.6)); wire(d, (o, -1.0), (o + 2.5, -1.0))
    el(d, E.Resistor, (o + 0.9, 3.6), (o + 0.9, -1.0), '1/sC', loc='bottom')
    el(d, E.SourceI, (o + 2.5, -1.0), (o + 2.5, 3.6), 'C·v(0⁻)', loc='bottom', color=HL)
    text(d, o + 1.3, -2.0, 'منبع جریان موازی')
    return d


@ckt('b15-lmodel')
def _():
    d = new(fontsize=12)
    dot(d, (0, 3.6), open=True, lab='+', loc='left')
    dot(d, (0, -1.0), open=True, lab='−', loc='left')
    el(d, E.Resistor, (0, 3.6), (0, 1.3), 'sL', loc='bottom')
    el(d, E.SourceV, (0, 1.3), (0, -1.0), 'L·i(0⁻)', loc='bottom', color=HL)
    text(d, 0, -2.0, 'منبع ولتاژ سری')
    o = 5
    dot(d, (o, 3.6), open=True, lab='+', loc='left')
    dot(d, (o, -1.0), open=True, lab='−', loc='left')
    wire(d, (o, 3.6), (o + 2.5, 3.6)); wire(d, (o, -1.0), (o + 2.5, -1.0))
    el(d, E.Resistor, (o + 0.9, 3.6), (o + 0.9, -1.0), 'sL', loc='bottom')
    el(d, E.SourceI, (o + 2.5, 3.6), (o + 2.5, -1.0), 'i(0⁻)/s', loc='bottom', color=HL)
    text(d, o + 1.3, -2.0, 'منبع جریان موازی')
    return d


@ckt('b15-z')
def _():
    d = new()
    dot(d, (0, 3), open=True, lab='a', loc='left')
    dot(d, (0, 0), open=True, lab='b', loc='left')
    wire(d, (0, 3), (2, 3)); wire(d, (0, 0), (5, 0))
    el(d, E.Resistor, (2, 3), (2, 1.5), '4Ω', loc='bottom')
    el(d, E.Inductor2, (2, 1.5), (2, 0), '2H', loc='bottom', loops=3)
    wire(d, (2, 3), (5, 3))
    el(d, E.Capacitor, (5, 3), (5, 0), '0.25F', loc='bottom')
    dot(d, (2, 3), (2, 0))
    return d


@ckt('b15-rlc')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10/s')
    el(d, E.Resistor, (0, 3), (3, 3), '3')
    el(d, E.Resistor, (3, 3), (3, 0), 's', loc='bottom')
    el(d, E.Resistor, (3, 0), (0, 0), '2/s', loc='bottom')
    d += E.LoopArrow(direction='cw', width=1.1, height=1.1).at((1.0, 0.95)).label('I(s)').color(MU)
    return d


@ckt('b15-zdep')
def _():
    d = new()
    dot(d, (0, 3), open=True, lab='a', loc='left')
    dot(d, (0, 0), open=True, lab='b', loc='left')
    wire(d, (0, 3), (2.5, 3))
    el(d, E.SourceControlledI, (2.5, 3), (2.5, 0), '2vₓ', loc='bottom', color=HL)
    el(d, E.Capacitor, (2.5, 3), (5.5, 3), '1F')
    el(d, E.Resistor, (5.5, 3), (5.5, 0), ('+', '1Ω  vₓ', '−'), loc='bottom')
    wire(d, (0, 0), (5.5, 0))
    dot(d, (2.5, 3), (2.5, 0))
    return d


@ckt('b15-lp')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'v_i')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    el(d, E.Capacitor, (3, 3), (3, 0), ('+', 'C   v_o', '−'), loc='bottom')
    wire(d, (0, 0), (3, 0))
    return d
