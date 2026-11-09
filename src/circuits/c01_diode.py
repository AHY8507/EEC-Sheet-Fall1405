from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('c1-sym')
def _():
    d = new(unit=3)
    d += E.Dot(open=True).label('A (آند، p)', loc='left')
    D = d.add(E.Diode().right().label(('+', 'v_D', '−'), loc='bottom'))
    d += E.Dot(open=True).label('K (کاتد، n)', loc='right')
    d += E.CurrentLabelInline(direction='in').at(D).label('i_D')
    return d


@ckt('c1-series')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'V')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    el(d, E.Diode, (3, 3), (3, 0), ('+', 'v_D', '−'), loc='bottom', color=HL)
    wire(d, (0, 0), (3, 0))
    return d


@ckt('c1-twod')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '5V')
    el(d, E.Resistor, (0, 3), (3, 3), '1kΩ')
    dot(d, (3, 3))
    text(d, 3, 3.5, 'A')
    el(d, E.Diode, (3, 3), (3, 1.5), 'D₁', loc='bottom', color=HL)
    el(d, E.Resistor, (3, 1.5), (3, 0), '1kΩ', loc='bottom')
    wire(d, (3, 3), (6, 3))
    el(d, E.Diode, (6, 3), (6, 1.5), 'D₂', loc='bottom', color=BL)
    el(d, E.SourceV, (6, 0), (6, 1.5), '2V', loc='bottom')
    wire(d, (0, 0), (6, 0))
    dot(d, (3, 0))
    return d


@ckt('c1-half')
def _():
    d = new()
    el(d, E.SourceSin, (0, 0), (0, 3), 'v_in')
    el(d, E.Diode, (0, 3), (3, 3), 'D', color=HL)
    el(d, E.Capacitor, (3, 3), (3, 0), 'C', loc='bottom', color=MU)
    wire(d, (3, 3), (5.5, 3))
    el(d, E.Resistor, (5.5, 3), (5.5, 0), ('+', 'R   v_o', '−'), loc='bottom')
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    return d


@ckt('c1-clip')
def _():
    d = new()
    el(d, E.SourceSin, (0, 0), (0, 3), 'v_in')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    el(d, E.Diode, (3, 3), (3, 1.5), 'D', loc='bottom', color=HL)
    el(d, E.SourceV, (3, 0), (3, 1.5), '2V', loc='bottom')
    wire(d, (3, 3), (5, 3)); wire(d, (0, 0), (5, 0))
    dot(d, (5, 3), open=True, lab='v_o', loc='right')
    dot(d, (5, 0), open=True)
    dot(d, (3, 3), (3, 0))
    return d


@ckt('c1-bridge')
def _():
    d = new(unit=2.2)
    top, left, right, bot = (3, 4), (1.2, 2), (4.8, 2), (3, 0)
    el(d, E.Diode, left, top, 'D₁', color=HL)
    el(d, E.Diode, bot, right, 'D₂', loc='bottom', color=HL)
    el(d, E.Diode, right, top, 'D₄', loc='bottom', color=BL)
    el(d, E.Diode, bot, left, 'D₃', color=BL)
    el(d, E.SourceSin, (-1.2, 1.0), (-1.2, 3.0), 'v_in')
    wire(d, (-1.2, 3.0), (-1.2, 3.6), (0.4, 3.6), (0.4, 2), left)
    wire(d, (-1.2, 1.0), (-1.2, -1.2), (6.2, -1.2), (6.2, 2), right)
    wire(d, top, (3, 5), (8, 5))
    wire(d, bot, (3, -0.6), (8, -0.6))
    el(d, E.Resistor, (8, 5), (8, -0.6), ('+', 'R_L  v_o', '−'), loc='bottom')
    dot(d, top, bot, left, right)
    return d


@ckt('c1-zener')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'V_s')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    el(d, E.Zener, (3, 0), (3, 3), 'V_Z', loc='bottom', color=HL)
    wire(d, (3, 3), (5.5, 3))
    el(d, E.Resistor, (5.5, 3), (5.5, 0), ('+', 'R_L  v_o', '−'), loc='bottom')
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    return d
