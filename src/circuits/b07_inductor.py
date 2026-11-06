from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('b7-sym')
def _():
    d = new(unit=3)
    d += E.Dot(open=True)
    L = d.add(E.Inductor2(loops=3).right().label(('+', 'v', '−'), loc='bottom').label('L', loc='top'))
    d += E.Dot(open=True)
    d += E.CurrentLabelInline(direction='in').at(L).label('i')
    return d


@ckt('b7-net')
def _():
    d = new()
    dot(d, (0, 3), open=True, lab='a', loc='left')
    dot(d, (0, 0), open=True, lab='b', loc='left')
    el(d, E.Inductor2, (0, 3), (3, 3), '4H', loops=3)
    el(d, E.Inductor2, (3, 3), (3, 0), '6H', loc='bottom', loops=3)
    wire(d, (3, 3), (5.5, 3))
    el(d, E.Inductor2, (5.5, 3), (5.5, 0), '3H', loc='bottom', loops=3)
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    wire(d, (0, 3), (0, 4.3), (8, 4.3))
    el(d, E.Inductor2, (8, 4.3), (8, 0), '12H', loc='bottom', loops=3, color=HL)
    wire(d, (5.5, 0), (8, 0))
    dot(d, (0, 3), (5.5, 0))
    return d


@ckt('b7-par')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '6V')
    el(d, E.Switch, (0, 3), (2.5, 3), 't = 0', action='close')
    L1 = el(d, E.Inductor2, (2.5, 3), (2.5, 0), 'L₁ = 2H', loc='bottom', loops=3)
    wire(d, (2.5, 3), (5.5, 3))
    L2 = el(d, E.Inductor2, (5.5, 3), (5.5, 0), 'L₂ = 6H', loc='bottom', loops=3)
    wire(d, (0, 0), (5.5, 0))
    dot(d, (2.5, 3), (2.5, 0))
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=True).at(L1).label('i₁')
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=True).at(L2).label('i₂')
    return d


@ckt('b7-spark')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Switch, (0, 3), (3, 3), 't = 0 (باز)', action='open', color=HL)
    el(d, E.Resistor, (3, 3), (6, 3), '6Ω')
    el(d, E.Inductor2, (6, 3), (6, 0), '0.2H', loc='bottom', loops=3)
    wire(d, (0, 0), (6, 0))
    return d


@ckt('b7-dual')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'v_s')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    el(d, E.Inductor2, (3, 3), (3, 0), 'L', loc='bottom', loops=3)
    el(d, E.Capacitor, (3, 0), (0, 0), 'C')
    text(d, 1.5, -1.0, 'RLC سری با منبع ولتاژ')
    text(d, 4.6, 1.5, '⟷')
    o = 6.2
    el(d, E.SourceI, (o, 0), (o, 3), 'i_s')
    wire(d, (o, 3), (o + 6, 3))
    wire(d, (o, 0), (o + 6, 0))
    el(d, E.Resistor, (o + 2, 3), (o + 2, 0), 'G', loc='bottom')
    el(d, E.Capacitor, (o + 4, 3), (o + 4, 0), 'C\' = L', loc='bottom')
    el(d, E.Inductor2, (o + 6, 3), (o + 6, 0), 'L\' = C', loc='bottom', loops=3)
    dot(d, (o + 2, 3), (o + 4, 3), (o + 2, 0), (o + 4, 0))
    text(d, o + 3, -1.0, 'GCL موازی با منبع جریان')
    return d
