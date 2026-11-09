from ck import ckt, new, E, HL, BL, MU, el, wire, dot, box, text


@ckt('b2-count')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'vs')
    el(d, E.Resistor, (0, 3), (3, 3), 'R₁')
    el(d, E.Resistor, (3, 3), (3, 0), 'R₂', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), 'R₃')
    el(d, E.Resistor, (6, 3), (6, 0), 'R₄', loc='bottom')
    wire(d, (0, 0), (6, 0))
    dot(d, (0, 3), lab='a', loc='left')
    dot(d, (3, 3), lab='b')
    dot(d, (6, 3), lab='c', loc='right')
    dot(d, (3, 0), lab='d', loc='bottom')
    text(d, 1.5, 1.5, '①', color=HL)
    text(d, 4.5, 1.5, '②', color=HL)
    return d


@ckt('b2-kcl')
def _():
    d = new(unit=2)
    c = (0, 0)
    d += E.Arrow().at((-3, 0)).to((-0.15, 0))
    d += E.Arrow().at((0, 2.6)).to((0, 0.15))
    d += E.Arrow().at((0.15, 0)).to((3, 0))
    d += E.Arrow().at((0, -0.15)).to((0, -2.6)).color(HL)
    d += E.Arrow().at((-0.12, 0.12)).to((-2, 2))
    text(d, -2.4, 0.45, 'i₁ = 3A')
    text(d, 0.9, 2.3, 'i₂ = 5A')
    text(d, 2.4, 0.45, 'i₃ = 2A')
    text(d, 0.85, -2.3, 'i₄ = ?', color=HL)
    text(d, -2.6, 2.2, 'i₅ = 4A')
    dot(d, c)
    return d


@ckt('b2-kvl')
def _():
    d = new()
    el(d, E.ResistorIEC, (0, 3), (3.5, 3), ('+', '5V', '−'))
    el(d, E.ResistorIEC, (3.5, 0), (3.5, 3), ('+', '12V', '−'), loc='bottom')
    el(d, E.ResistorIEC, (3.5, 0), (0, 0), ('+', 'vₓ', '−'), loc='bottom', color=HL)
    el(d, E.ResistorIEC, (0, 0), (0, 3), ('+', '3V', '−'), loc='top')
    d += E.LoopArrow(direction='cw', width=1.1, height=1.1).at((1.2, 0.95)).color(MU)
    return d


@ckt('b2-loop')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '24V')
    el(d, E.Resistor, (0, 3), (3.5, 3), '2Ω')
    el(d, E.SourceV, (3.5, 0), (3.5, 3), '12V', loc='bottom')
    el(d, E.Resistor, (3.5, 0), (0, 0), '4Ω', loc='bottom')
    d += E.LoopArrow(direction='cw', width=1.1, height=1.1).at((1.2, 0.95)).label('i').color(MU)
    return d


@ckt('b2-pair')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '6A')
    el(d, E.Resistor, (2.5, 3), (2.5, 0), '3Ω', loc='bottom')
    el(d, E.SourceI, (5, 3), (5, 0), '2A', loc='bottom')
    el(d, E.Resistor, (7.5, 3), (7.5, 0), '6Ω', loc='bottom')
    wire(d, (0, 3), (7.5, 3))
    wire(d, (0, 0), (7.5, 0))
    dot(d, (2.5, 3), (5, 3), (2.5, 0), (5, 0))
    return d


@ckt('b2-ladder')
def _():
    d = new()
    dot(d, (0, 3), open=True, lab='a', loc='left')
    dot(d, (0, 0), open=True, lab='b', loc='left')
    el(d, E.Resistor, (0, 3), (3, 3), '2Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '6Ω', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '1Ω')
    el(d, E.Resistor, (6, 3), (6, 0), '3Ω', loc='bottom')
    wire(d, (6, 3), (8.5, 3))
    el(d, E.Resistor, (8.5, 3), (8.5, 0), '6Ω', loc='bottom')
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3, 3), (6, 3), (3, 0), (6, 0))
    text(d, 3, 3.5, 'x')
    text(d, 6, 3.5, 'y')
    return d


@ckt('b2-loaded')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3.2), '12V')
    el(d, E.Resistor, (0, 3.2), (3, 3.2), 'R₁ = 10k')
    el(d, E.Resistor, (3, 3.2), (3, 0), 'R₂ = 10k', loc='bottom')
    wire(d, (3, 3.2), (6, 3.2))
    el(d, E.Resistor, (6, 3.2), (6, 0), 'R_L', loc='bottom', color=HL)
    wire(d, (0, 0), (6, 0))
    dot(d, (3, 3.2), (3, 0))
    return d


@ckt('b2-srctrans')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (3, 3), '3Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '6Ω', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '2Ω')
    el(d, E.SourceI, (6, 0), (6, 3), '1A', loc='bottom')
    wire(d, (6, 3), (8.5, 3))
    el(d, E.Resistor, (8.5, 3), (8.5, 0), 'R_L = 4Ω', loc='bottom', color=HL)
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3, 3), (6, 3), (3, 0), (6, 0))
    text(d, 3, 3.55, 'a')
    text(d, 6, 3.55, 'b')
    return d


@ckt('b2-yd')
def _():
    d = new(unit=2.2)
    # Delta
    A, B, C = (1.5, 3.2), (0, 0.6), (3, 0.6)
    el(d, E.Resistor, B, A, 'Rc')
    el(d, E.Resistor, A, C, 'Rb')
    el(d, E.Resistor, B, C, 'Ra', loc='bottom')
    dot(d, A, lab='a'); dot(d, B, lab='b', loc='left'); dot(d, C, lab='c', loc='right')
    text(d, 1.5, -0.6, 'مثلث (Δ)')
    # Y
    o = 6.2
    A2, B2, C2, N = (o + 1.5, 3.2), (o, 0.6), (o + 3, 0.6), (o + 1.5, 1.6)
    el(d, E.Resistor, A2, N, 'R₁', loc='bottom')
    el(d, E.Resistor, B2, N, 'R₂')
    el(d, E.Resistor, C2, N, 'R₃', loc='bottom')
    dot(d, A2, lab='a'); dot(d, B2, lab='b', loc='left'); dot(d, C2, lab='c', loc='right')
    text(d, o + 1.5, -0.6, 'ستاره (Y)')
    return d


@ckt('b2-bridge')
def _():
    d = new(unit=2.4)
    a, c, dd, b = (2, 5), (0, 2.5), (4, 2.5), (2, 0)
    el(d, E.Resistor, a, c, '10Ω')
    el(d, E.Resistor, a, dd, '20Ω')
    el(d, E.Resistor, c, dd, '30Ω', loc='bottom', color=HL)
    el(d, E.Resistor, c, b, '15Ω', loc='bottom')
    el(d, E.Resistor, dd, b, '10Ω', loc='bottom')
    wire(d, a, (2, 6))
    wire(d, b, (2, -1))
    dot(d, (2, 6), open=True, lab='A', loc='right')
    dot(d, (2, -1), open=True, lab='B', loc='right')
    dot(d, a, c, dd, b)
    text(d, -0.5, 2.5, 'c')
    text(d, 4.5, 2.5, 'd')
    return d


@ckt('b2-dep-loop')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    R = el(d, E.Resistor, (0, 3), (3.5, 3), '2Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    el(d, E.SourceControlledV, (3.5, 0), (3.5, 3), '4i', loc='bottom', color=HL)
    el(d, E.Resistor, (3.5, 0), (0, 0), '4Ω', loc='bottom')
    return d
