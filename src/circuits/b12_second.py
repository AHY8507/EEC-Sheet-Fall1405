from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('b12-par')
def _():
    d = new()
    el(d, E.Resistor, (0, 3), (0, 0), 'R', loc='top')
    el(d, E.Inductor2, (2.6, 3), (2.6, 0), 'L', loc='bottom', loops=3)
    el(d, E.Capacitor, (5.2, 3), (5.2, 0), ('+', 'C   v', '−'), loc='bottom')
    wire(d, (0, 3), (5.2, 3)); wire(d, (0, 0), (5.2, 0))
    dot(d, (2.6, 3), (2.6, 0))
    return d


@ckt('b12-ser')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'v_s')
    R = el(d, E.Resistor, (0, 3), (3, 3), 'R')
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    el(d, E.Inductor2, (3, 3), (3, 0), 'L', loc='bottom', loops=3)
    el(d, E.Capacitor, (3, 0), (0, 0), ('+', 'C   v_C', '−'), loc='bottom')
    return d


@ckt('b12-imp')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), 'δ(t)', color=HL)
    wire(d, (0, 3), (7.8, 3)); wire(d, (0, 0), (7.8, 0))
    el(d, E.Resistor, (2.6, 3), (2.6, 0), '1Ω', loc='bottom')
    el(d, E.Inductor2, (5.2, 3), (5.2, 0), '1H', loc='bottom', loops=3)
    el(d, E.Capacitor, (7.8, 3), (7.8, 0), ('+', '1F   v', '−'), loc='bottom')
    dot(d, (2.6, 3), (5.2, 3), (2.6, 0), (5.2, 0))
    return d


@ckt('b12-dep')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'v_s')
    R = el(d, E.Resistor, (0, 3), (3, 3), '1Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    el(d, E.Inductor2, (3, 3), (6, 3), '1H', loops=3)
    el(d, E.SourceControlledV, (6, 0), (6, 3), 'k·i', loc='bottom', color=HL)
    el(d, E.Capacitor, (6, 0), (0, 0), '1F', loc='bottom')
    return d


@ckt('b12-alg')
def _():
    """Worked example of the five-step algorithm: 12 V switched onto a series RLC at t = 0."""
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Switch, (0, 3), (2.4, 3), 't = 0', action='close', color=HL)
    R = el(d, E.Resistor, (2.4, 3), (5.2, 3), '6Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    el(d, E.Inductor2, (5.2, 3), (5.2, 0), '1H', loc='bottom', loops=3)
    el(d, E.Capacitor, (5.2, 0), (0, 0), ('+', '0.2F   v_C', '−'), loc='bottom')
    return d
