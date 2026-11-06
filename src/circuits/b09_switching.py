from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('b9-rc')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (2.6, 3), '2Ω')
    el(d, E.Switch, (2.6, 3), (5, 3), 't = 0', action='open', color=HL)
    el(d, E.Capacitor, (5, 3), (5, 0), ('+', 'C = 0.5F  v_C', '−'), loc='bottom')
    wire(d, (5, 3), (8, 3))
    el(d, E.Resistor, (8, 3), (8, 0), '4Ω', loc='bottom')
    wire(d, (0, 0), (8, 0))
    dot(d, (5, 3), (5, 0))
    text(d, 5, 3.5, 'a')
    return d


@ckt('b9-rl')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10V')
    el(d, E.Switch, (0, 3), (2.6, 3), 't = 0', action='close', color=HL)
    el(d, E.Resistor, (2.6, 3), (5.2, 3), '5Ω')
    L = el(d, E.Inductor2, (5.2, 3), (5.2, 0), '2H', loc='bottom', loops=3)
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=False).at(L).label('i_L')
    wire(d, (5.2, 3), (8, 3))
    el(d, E.Resistor, (8, 3), (8, 0), '20Ω', loc='bottom')
    wire(d, (0, 0), (8, 0))
    dot(d, (5.2, 3), (5.2, 0))
    return d


@ckt('b9-rlc')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10V')
    el(d, E.Resistor, (0, 3), (2.6, 3), 'R₁ = 2Ω')
    el(d, E.Switch, (2.6, 3), (5, 3), 't = 0', action='open', color=HL)
    el(d, E.Capacitor, (5, 3), (5, 0), ('+', 'C = 0.25F', '−'), loc='bottom')
    wire(d, (5, 3), (8.5, 3))
    L = el(d, E.Inductor2, (8.5, 3), (8.5, 1.4), 'L = 1H', loc='bottom', loops=3)
    el(d, E.Resistor, (8.5, 1.4), (8.5, 0), 'R₂ = 3Ω', loc='bottom')
    wire(d, (0, 0), (8.5, 0))
    dot(d, (5, 3), (5, 0))
    text(d, 5, 3.5, 'a')
    d += E.CurrentLabel(ofst=0.5, length=0.9, top=False).at(L).label('i_L')
    return d


@ckt('b9-imp-c')
def _():
    d = new()
    el(d, E.Capacitor, (0, 0), (0, 3), ('−', 'C₁ = 2F (6V)', '+'))
    el(d, E.Switch, (0, 3), (3.5, 3), 't = 0', action='close', color=HL)
    el(d, E.Capacitor, (3.5, 0), (3.5, 3), ('−', 'C₂ = 1F (0V)', '+'), loc='bottom')
    wire(d, (0, 0), (3.5, 0))
    return d
