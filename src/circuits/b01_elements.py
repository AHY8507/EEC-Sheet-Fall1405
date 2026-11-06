from ck import ckt, new, E, HL, BL, MU, box, text


@ckt('b1-ref')
def _():
    d = new(unit=3)
    d += E.Dot(open=True).label('a', loc='left')
    R = d.add(E.ResistorIEC().right().label(('+', 'v(t)', '−'), loc='bottom').label('المان', loc='top'))
    d += E.Dot(open=True).label('b', loc='right')
    d += E.CurrentLabelInline(direction='in').at(R).label('i(t)')
    return d


@ckt('b1-sources')
def _():
    d = new(unit=2.2, fontsize=12)
    items = [(E.SourceV, 'vs', 'ولتاژ مستقل'), (E.SourceI, 'is', 'جریان مستقل'),
             (E.SourceControlledV, 'μ·vx', 'VCVS'), (E.SourceControlledV, 'r·ix', 'CCVS'),
             (E.SourceControlledI, 'g·vx', 'VCCS'), (E.SourceControlledI, 'β·ix', 'CCCS')]
    for k, (el, val, name) in enumerate(items):
        x = k * 3.0
        d += el().at((x, 0)).up().label(val, loc='bottom')
        text(d, x, -0.7, name)
    return d


@ckt('b1-rule-v')
def _():
    d = new()
    d += E.SourceV().at((0, 0)).up().label('Vs')
    d += E.Line().at((0, 2.6)).to((2, 2.6))
    d += E.Dot().at((2, 2.6))
    d += E.Resistor().at((2, 2.6)).down().label('R', loc='bottom').color(HL)
    d += E.Dot().at((2, 0))
    d += E.Line().at((2, 2.6)).to((4, 2.6))
    d += E.Line().at((4, 0)).to((0, 0))
    box(d, 4, -0.5, 6.8, 3.1, 'بقیه مدار')
    return d


@ckt('b1-rule-i')
def _():
    d = new()
    d += E.SourceI().at((0, 0)).up().label('Is')
    d += E.Resistor().at((0, 2.6)).right().label('R').color(HL)
    d += E.Line().at((2.6, 2.6)).to((4, 2.6))
    d += E.Line().at((4, 0)).to((0, 0))
    box(d, 4, -0.5, 6.8, 3.1, 'بقیه مدار')
    return d


from ck import el, wire, dot, gnd  # noqa: E402


@ckt('b1-power')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (3.5, 3), 'R₁ = 2Ω')
    dot(d, (3.5, 3), lab='a')
    el(d, E.Resistor, (3.5, 3), (3.5, 0), 'R₂ = 6Ω', loc='bottom')
    wire(d, (3.5, 3), (7, 3))
    el(d, E.SourceI, (7, 0), (7, 3), '1A', loc='bottom')
    wire(d, (0, 0), (7, 0))
    dot(d, (3.5, 0))
    return d


@ckt('b1-dep')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '2A')
    wire(d, (0, 3), (3, 3))
    R = el(d, E.Resistor, (3, 3), (3, 0), '5Ω', loc='top')
    d += E.CurrentLabel(ofst=0.45, length=1.1).at(R).label('iₓ')
    wire(d, (0, 0), (8, 0))
    el(d, E.SourceControlledV, (6, 0), (6, 3), '3·iₓ', color=HL)
    el(d, E.Resistor, (6, 3), (9, 3), '4Ω')
    wire(d, (9, 3), (9, 0), (8, 0))
    dot(d, (3, 0), (6, 0))
    return d
