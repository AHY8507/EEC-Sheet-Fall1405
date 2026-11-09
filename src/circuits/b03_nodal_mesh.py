from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, box


@ckt('b3-n1')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '4.5A')
    wire(d, (0, 3), (5, 3))
    el(d, E.Resistor, (2.5, 3), (2.5, 0), '2Ω', loc='bottom')
    el(d, E.Resistor, (5, 3), (8, 3), '4Ω')
    el(d, E.Resistor, (8, 3), (8, 0), '6Ω', loc='bottom')
    wire(d, (8, 3), (10.5, 3))
    el(d, E.SourceI, (10.5, 0), (10.5, 3), '0.5A', loc='bottom')
    wire(d, (0, 0), (10.5, 0))
    dot(d, (2.5, 3), (8, 3), (2.5, 0), (8, 0))
    text(d, 3.4, 3.45, 'v₁', color=HL)
    text(d, 8.6, 3.45, 'v₂', color=HL)
    gnd(d, (5, 0))
    return d


@ckt('b3-n2')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10V')
    el(d, E.Resistor, (0, 3), (3, 3), '2Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '4Ω', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '2Ω')
    el(d, E.Resistor, (6, 3), (6, 0), '2Ω', loc='bottom')
    wire(d, (6, 3), (8.5, 3))
    el(d, E.SourceI, (8.5, 0), (8.5, 3), '2A', loc='bottom')
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3, 3), (6, 3), (3, 0), (6, 0))
    text(d, -0.2, 3.45, '①')
    text(d, 3, 3.5, 'v₂', color=HL)
    text(d, 6, 3.5, 'v₃', color=HL)
    gnd(d, (4.5, 0))
    return d


@ckt('b3-super')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '6A')
    wire(d, (0, 3), (2.5, 3))
    el(d, E.Resistor, (2.5, 3), (2.5, 0), '3Ω', loc='bottom')
    el(d, E.SourceV, (2.5, 3), (6, 3), ('−', '6V', '+'), color=HL)
    el(d, E.Resistor, (6, 3), (6, 0), '6Ω', loc='bottom')
    wire(d, (0, 0), (6, 0))
    dot(d, (2.5, 3), (6, 3), (2.5, 0))
    text(d, 2.5, 3.6, 'v₁')
    text(d, 6, 3.6, 'v₂')
    gnd(d, (4.2, 0))
    box(d, 1.9, 2.3, 6.6, 4.1, color=MU, dash=True)
    text(d, 4.25, 1.9, 'ابرگره', color=MU)
    return d


@ckt('b3-ndep')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (3, 3), '2Ω')
    el(d, E.Resistor, (3, 3), (3, 0), ('+', '4Ω  vₓ', '−'), loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '2Ω')
    el(d, E.Resistor, (6, 3), (6, 0), '4Ω', loc='bottom')
    wire(d, (6, 3), (8.5, 3))
    el(d, E.SourceControlledI, (8.5, 0), (8.5, 3), 'vₓ/8', loc='bottom', color=HL)
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3, 3), (6, 3), (3, 0), (6, 0))
    text(d, 3, 3.5, 'v₁')
    text(d, 6, 3.5, 'v₂')
    gnd(d, (4.5, 0))
    return d


@ckt('b3-m1')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '24V')
    el(d, E.Resistor, (0, 3), (3.5, 3), '4Ω')
    el(d, E.Resistor, (3.5, 3), (3.5, 0), '6Ω', loc='bottom')
    el(d, E.Resistor, (3.5, 3), (7, 3), '2Ω')
    el(d, E.SourceV, (7, 0), (7, 3), '10V', loc='bottom')
    wire(d, (0, 0), (7, 0))
    dot(d, (3.5, 3), (3.5, 0))
    d += E.LoopArrow(direction='cw', width=1.0, height=1.0).at((1.3, 1.0)).label('I₁').color(MU)
    d += E.LoopArrow(direction='cw', width=1.0, height=1.0).at((4.8, 1.0)).label('I₂').color(MU)
    return d


@ckt('b3-msuper')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (3.5, 3), '2Ω')
    el(d, E.SourceI, (3.5, 0), (3.5, 3), '3A', loc='bottom', color=HL)
    el(d, E.Resistor, (3.5, 3), (7, 3), '4Ω')
    el(d, E.Resistor, (7, 3), (7, 0), '2Ω', loc='bottom')
    wire(d, (0, 0), (7, 0))
    dot(d, (3.5, 3), (3.5, 0))
    d += E.LoopArrow(direction='cw', width=1.0, height=1.0).at((1.3, 1.0)).label('I₁').color(MU)
    d += E.LoopArrow(direction='cw', width=1.0, height=1.0).at((4.8, 1.0)).label('I₂').color(MU)
    return d


@ckt('b3-mdep')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10V')
    el(d, E.Resistor, (0, 3), (3.5, 3), '2Ω')
    R = el(d, E.Resistor, (3.5, 3), (3.5, 0), '4Ω', loc='top')
    d += E.CurrentLabel(ofst=0.45, length=1.1).at(R).label('iₓ')
    el(d, E.Resistor, (3.5, 3), (7, 3), '2Ω')
    el(d, E.SourceControlledV, (7, 0), (7, 3), '2iₓ', loc='bottom', color=HL)
    wire(d, (0, 0), (7, 0))
    dot(d, (3.5, 3), (3.5, 0))
    d += E.LoopArrow(direction='cw', width=1.0, height=1.0).at((1.3, 1.0)).label('I₁').color(MU)
    d += E.LoopArrow(direction='cw', width=1.0, height=1.0).at((4.8, 1.0)).label('I₂').color(MU)
    return d


@ckt('b3-m3')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '16V')
    el(d, E.Resistor, (0, 3), (3.2, 3), '6Ω')
    el(d, E.Resistor, (3.2, 3), (3.2, 0), '4Ω', loc='bottom')
    el(d, E.Resistor, (3.2, 3), (5, 3), '2Ω')
    el(d, E.SourceV, (5, 3), (7, 3), '4V')
    el(d, E.Resistor, (7, 3), (7, 0), '6Ω', loc='bottom')
    el(d, E.Resistor, (7, 3), (10, 3), '3Ω')
    el(d, E.SourceV, (10, 0), (10, 3), '6V', loc='bottom')
    wire(d, (0, 0), (10, 0))
    dot(d, (3.2, 3), (7, 3), (3.2, 0), (7, 0))
    for x, lab in ((1.1, 'I₁'), (4.6, 'I₂'), (8.0, 'I₃')):
        d += E.LoopArrow(direction='cw', width=0.9, height=0.9).at((x, 1.0)).label(lab).color(MU)
    return d
