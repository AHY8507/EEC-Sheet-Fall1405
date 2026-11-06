from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('b6-sym')
def _():
    d = new(unit=3)
    d += E.Dot(open=True)
    C = d.add(E.Capacitor().right().label(('+', 'v', '−'), loc='bottom').label('C', loc='top'))
    d += E.Dot(open=True)
    d += E.CurrentLabelInline(direction='in').at(C).label('i')
    return d


@ckt('b6-net')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '24V')
    el(d, E.Capacitor, (0, 3), (3, 3), 'C₁ = 6µF')
    el(d, E.Capacitor, (3, 3), (3, 0), 'C₂ = 3µF', loc='bottom')
    wire(d, (3, 3), (6, 3))
    el(d, E.Capacitor, (6, 3), (6, 0), 'C₃ = 9µF', loc='bottom')
    wire(d, (0, 0), (6, 0))
    dot(d, (3, 3), (3, 0))
    return d


@ckt('b6-share')
def _():
    d = new()
    el(d, E.Capacitor, (0, 0), (0, 3), ('−', 'C₁', '+'))
    el(d, E.Switch, (0, 3), (3.5, 3), 't = 0', action='close')
    el(d, E.Capacitor, (3.5, 0), (3.5, 3), ('−', 'C₂', '+'), loc='bottom')
    wire(d, (0, 0), (3.5, 0))
    return d


@ckt('b6-share-r')
def _():
    d = new()
    el(d, E.Capacitor, (0, 0), (0, 3), ('−', 'C₁', '+'))
    el(d, E.Switch, (0, 3), (2.5, 3), 't = 0', action='close')
    R = el(d, E.Resistor, (2.5, 3), (5, 3), 'R', color=HL)
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    el(d, E.Capacitor, (5, 0), (5, 3), ('−', 'C₂', '+'), loc='bottom')
    wire(d, (0, 0), (5, 0))
    return d


@ckt('b6-series-ic')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '2A')
    el(d, E.Capacitor, (0, 3), (3, 3), ('+', 'C₁ = 1F', '−'))
    el(d, E.Capacitor, (3, 3), (3, 0), ('+', 'C₂ = 4F', '−'), loc='bottom')
    wire(d, (0, 0), (3, 0))
    return d
