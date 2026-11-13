"""Homework 2 (first- and second-order circuits): the ten circuits of the problem sheet, redrawn."""
from ck import ckt, new, E, HL, BL, el, wire, dot, gnd, text


@ckt('h2-p1')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 4.5), 'vᵢₙ')
    wire(d, (0, 4.5), (1.2, 4.5))
    el(d, E.SourceControlledV, (1.2, 4.5), (3.4, 4.5), '2vₓ', color=HL)
    el(d, E.Capacitor, (3.4, 4.5), (5.4, 4.5), 'C₁ = 1F')
    wire(d, (5.4, 4.5), (6.2, 4.5))
    wire(d, (1.2, 4.5), (1.2, 2.8), (2.2, 2.8))
    el(d, E.Resistor, (2.2, 2.8), (4.6, 2.8), '6Ω', loc='bottom')
    wire(d, (4.6, 2.8), (6.2, 2.8), (6.2, 4.5), (7.2, 4.5))
    el(d, E.Capacitor, (7.2, 4.5), (7.2, 0), 'C₂ = 1F', loc='bottom')
    d += E.Resistor().endpoints((7.2, 4.5), (9.8, 4.5)).label(('+', 'vₓ', '−')).label('0.5Ω', loc='bottom')
    el(d, E.Resistor, (9.8, 4.5), (9.8, 0), ('+', '1Ω   vₒᵤₜ', '−'), loc='bottom')
    wire(d, (0, 0), (9.8, 0))
    dot(d, (1.2, 4.5), (6.2, 4.5), (7.2, 4.5), (7.2, 0))
    text(d, 6.2, 5.0, 'B')
    text(d, 9.8, 5.0, 'out')
    return d


@ckt('h2-p2')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 2), '10V')
    el(d, E.Resistor, (0, 2), (0, 4), '1Ω')
    el(d, E.Switch, (0, 4), (2.4, 4), 't = 0 (باز می‌شود)', action='open', color=HL)
    wire(d, (2.4, 4), (10.4, 4))
    el(d, E.Resistor, (3.2, 4), (3.2, 0), 'R', loc='bottom')
    L = el(d, E.Inductor2, (6.0, 4), (6.0, 0), '0.25H', loc='bottom', loops=3)
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=False).at(L).label('i_L')
    el(d, E.Capacitor, (8.4, 4), (8.4, 0), ('+', '1F   v_C', '−'), loc='bottom')
    el(d, E.SourceI, (10.4, 0), (10.4, 4), '2u(−t) A', loc='bottom')
    wire(d, (0, 0), (10.4, 0))
    dot(d, (3.2, 4), (6.0, 4), (8.4, 4), (3.2, 0), (6.0, 0), (8.4, 0))
    return d


@ckt('h2-p3')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3.5), '10V')
    wire(d, (0, 3.5), (1.4, 3.5))
    wire(d, (1.4, 2), (1.4, 5))
    el(d, E.Resistor, (1.4, 5), (4.6, 5), '3Ω')
    el(d, E.Capacitor, (1.4, 2), (4.6, 2), 'C₁ = 2F', loc='bottom')
    el(d, E.Switch, (4.6, 5), (4.6, 2), 't = 0', action='close', color=HL, loc='bottom')
    el(d, E.Resistor, (4.6, 5), (8.2, 5), '2Ω')
    el(d, E.Capacitor, (4.6, 2), (8.2, 2), 'C₂ = 3F', loc='bottom')
    wire(d, (4.6, 5), (4.6, 6.3))
    el(d, E.Capacitor, (4.6, 6.3), (8.2, 6.3), 'C₃ = 2F')
    wire(d, (8.2, 6.3), (8.2, 0))
    el(d, E.Resistor, (4.6, 2), (4.6, 0), ('+', '3Ω   v(t)', '−'), loc='bottom')
    wire(d, (0, 0), (8.2, 0))
    dot(d, (1.4, 3.5), (4.6, 5), (4.6, 2), (8.2, 5), (8.2, 2), (4.6, 0))
    text(d, 1.0, 5.3, 'L')
    text(d, 4.25, 5.35, 'T', color=BL)
    text(d, 4.2, 1.7, 'B', color=BL)
    return d


@ckt('h2-p4')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 4), '10u(t)')
    wire(d, (0, 4), (1.6, 4))
    el(d, E.Resistor, (1.6, 4), (4.2, 4), '2Ω')
    el(d, E.Switch, (1.6, 4), (1.6, 2.2), 't = 0', action='open', color=HL, loc='bottom')
    el(d, E.Capacitor, (1.6, 2.2), (1.6, 0), '2F', loc='bottom')
    el(d, E.Capacitor, (1.6, 2.2), (4.2, 2.2), '1F', loc='bottom')
    wire(d, (4.2, 2.2), (4.2, 4))
    el(d, E.Resistor, (4.2, 4), (6.8, 4), '4Ω')
    d += E.Capacitor().endpoints((4.2, 2.2), (6.8, 2.2)).label(('+', 'v_C', '−'), loc='bottom').label('2F').color(HL)
    wire(d, (6.8, 2.2), (6.8, 4))
    el(d, E.Resistor, (6.8, 4), (8.4, 4), '8Ω')
    el(d, E.Capacitor, (8.4, 4), (10, 4), '1F')
    el(d, E.Capacitor, (6.8, 2.2), (10, 2.2), '4F', loc='bottom')
    wire(d, (10, 2.2), (10, 4))
    el(d, E.SourceV, (10, 0), (10, 2.2), '2u(−t)', loc='bottom')
    wire(d, (0, 0), (10, 0))
    dot(d, (1.6, 4), (1.6, 2.2), (4.2, 4), (6.8, 4), (4.2, 2.2), (6.8, 2.2), (10, 2.2), (1.6, 0))
    text(d, 1.25, 4.4, 'A')
    text(d, 1.2, 2.5, 'P')
    text(d, 4.2, 4.45, 'M', color=BL)
    text(d, 6.8, 4.45, 'N', color=BL)
    text(d, 10.4, 4.3, 'K')
    return d


@ckt('h2-p5')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10u(t)')
    el(d, E.Resistor, (0, 3), (2.6, 3), '1Ω')
    wire(d, (2.6, 3), (2.6, 4.7))
    el(d, E.Resistor, (2.6, 4.7), (5.4, 4.7), '3Ω')
    wire(d, (5.4, 4.7), (5.4, 3))
    d += E.Capacitor().endpoints((2.6, 3), (5.4, 3)).label(('+', '1F   v_C', '−'))
    L1 = el(d, E.Inductor2, (2.6, 3), (2.6, 1.5), ('+', '1H', '−'), loc='top', loops=3)
    el(d, E.Resistor, (2.6, 1.5), (2.6, 0), '2Ω', loc='bottom')
    L2 = el(d, E.Inductor2, (5.4, 3), (5.4, 1.5), ('+', '1H', '−'), loc='bottom', loops=3)
    el(d, E.Resistor, (5.4, 1.5), (5.4, 0), '2Ω', loc='bottom')
    d += E.CurrentLabel(ofst=0.45, length=0.8, top=True).at(L1).label('i₁')
    d += E.CurrentLabel(ofst=0.45, length=0.8, top=False).at(L2).label('i₂')
    wire(d, (5.4, 3), (7.6, 3))
    el(d, E.SourceI, (7.6, 0), (7.6, 3), '5u(t)', loc='bottom')
    wire(d, (0, 0), (7.6, 0))
    dot(d, (2.6, 3), (5.4, 3), (2.6, 0), (5.4, 0))
    text(d, 2.25, 3.35, 'X', color=BL)
    text(d, 5.75, 3.35, 'Y', color=BL)
    return d


@ckt('h2-u1')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 4), '6u(t)')
    wire(d, (0, 4), (8.8, 4))
    el(d, E.Resistor, (1.8, 4), (1.8, 0), '1Ω', loc='bottom')
    el(d, E.ResistorVar, (4.0, 4), (4.0, 2), 'R(t)', loc='bottom')
    L = el(d, E.Inductor2, (4.0, 2), (4.0, 0), '1H', loc='bottom', loops=3)
    d += E.CurrentLabel(ofst=0.45, length=0.8, top=False).at(L).label('i_L')
    el(d, E.Capacitor, (6.1, 4), (6.1, 0), ('+', '0.5F  v_C', '−'), loc='bottom')
    el(d, E.SourceI, (8.8, 0), (8.8, 4), '12u(−t)', loc='bottom')
    el(d, E.Switch, (8.8, 4), (11.2, 4), 't = 3s', action='close', color=HL)
    el(d, E.SourceV, (11.2, 0), (11.2, 4), '30V', loc='bottom')
    wire(d, (0, 0), (11.2, 0))
    dot(d, (1.8, 4), (4.0, 4), (6.1, 4), (8.8, 4), (1.8, 0), (4.0, 0), (6.1, 0), (8.8, 0))
    return d


@ckt('h2-u2')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3.2), '20u(−t)V')
    el(d, E.Resistor, (0, 3.2), (2.6, 3.2), '6Ω')
    el(d, E.Capacitor, (2.6, 3.2), (2.6, 0), ('+', '0.5F  v_C', '−'), loc='bottom')
    wire(d, (2.6, 3.2), (5.0, 3.2))
    el(d, E.ResistorVar, (5.0, 3.2), (5.0, 0), 'R', loc='bottom')
    el(d, E.Switch, (5.0, 3.2), (7.0, 3.2), 't = 0', action='close', color=HL)
    el(d, E.SourceControlledV, (9.2, 3.2), (7.0, 3.2), '2vₓ', color=HL)
    el(d, E.Resistor, (9.2, 3.2), (9.2, 0), ('+', '2Ω   vₓ', '−'), loc='bottom')
    wire(d, (9.2, 3.2), (11.2, 3.2))
    el(d, E.SourceI, (11.2, 0), (11.2, 3.2), '2A', loc='bottom')
    wire(d, (0, 0), (11.2, 0))
    dot(d, (2.6, 3.2), (5.0, 3.2), (9.2, 3.2), (2.6, 0), (5.0, 0), (9.2, 0))
    text(d, 2.6, 3.65, 'A', color=BL)
    text(d, 9.2, 3.65, 'B', color=BL)
    return d


@ckt('h2-u3')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3.4), '10V')
    wire(d, (0, 3.4), (1.6, 3.4))
    el(d, E.SourceV, (2.6, 0), (2.6, 2.4), '20V', loc='bottom')
    dot(d, (1.6, 3.4), (2.6, 2.4), open=True)
    dot(d, (2.6, 3.4))
    wire(d, (2.6, 3.4), (2.6, 2.4), color=HL)
    d += E.Line().at((2.6, 3.4)).to((1.7, 3.4)).linestyle('--').color(HL)
    text(d, 2.1, 3.95, 't = 0', color=HL)
    el(d, E.Resistor, (2.6, 3.4), (5.6, 3.4), '5Ω')
    L = el(d, E.Inductor2, (5.6, 3.4), (5.6, 0), '4H', loc='bottom', loops=3)
    d += E.CurrentLabel(ofst=0.45, length=0.9, top=False).at(L).label('i_L')
    wire(d, (5.6, 3.4), (7.6, 3.4))
    el(d, E.Resistor, (7.6, 3.4), (7.6, 0), '20Ω', loc='bottom')
    el(d, E.Switch, (7.6, 3.4), (9.8, 3.4), 't = 1s', action='close', color=HL)
    el(d, E.Resistor, (9.8, 3.4), (9.8, 0), '4Ω', loc='bottom')
    wire(d, (9.8, 3.4), (11.6, 3.4))
    el(d, E.SourceI, (11.6, 0), (11.6, 3.4), '4A', loc='bottom')
    wire(d, (0, 0), (11.6, 0))
    dot(d, (5.6, 3.4), (7.6, 3.4), (9.8, 3.4), (5.6, 0), (7.6, 0), (9.8, 0))
    text(d, 5.6, 3.85, 'X', color=BL)
    return d


@ckt('h2-u4')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'v_s(t)')
    wire(d, (0, 3), (1.6, 3))
    el(d, E.Resistor, (1.6, 3), (4.6, 3), '3Ω', loc='bottom')
    wire(d, (1.6, 3), (1.6, 5.0))
    L = el(d, E.Inductor2, (1.6, 5.0), (4.6, 5.0), '2/3 H', loops=3)
    wire(d, (4.6, 5.0), (4.6, 3), (6.4, 3))
    el(d, E.Resistor, (6.4, 3), (6.4, 0), ('+', '6Ω   vₒ', '−'), loc='bottom')
    wire(d, (0, 0), (6.4, 0))
    dot(d, (1.6, 3), (4.6, 3))
    text(d, 1.25, 2.6, 'a', color=BL)
    text(d, 4.95, 2.6, 'b', color=BL)
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=False).at(L).label('i_L')
    return d


@ckt('h2-u5')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), 'u(t)')
    wire(d, (0, 3), (3.4, 3))
    R1 = el(d, E.Resistor, (1.7, 3), (1.7, 0), '2Ω', loc='bottom')
    d += E.CurrentLabel(ofst=0.45, length=0.8, top=False).at(R1).label('i')
    el(d, E.Capacitor, (3.4, 3), (3.4, 0), ('+', '1F  v_C', '−'), loc='bottom')
    el(d, E.Resistor, (3.4, 3), (6.2, 3), '2Ω')
    el(d, E.SourceControlledV, (6.2, 0), (6.2, 3), '4i', loc='bottom', color=HL)
    wire(d, (0, 0), (6.2, 0))
    dot(d, (1.7, 3), (3.4, 3), (1.7, 0), (3.4, 0))
    text(d, 6.6, 3.35, 'D', color=BL)
    return d


@ckt('h2-p4s')
def _():
    """Problem 4 for t > 0: switch open, 2u(-t) = 0 (K grounded), P's two capacitors merged."""
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3.4), '10A')
    wire(d, (0, 3.4), (1.8, 3.4))
    el(d, E.Capacitor, (1.8, 3.4), (1.8, 0), ('', '⅔F', ''), loc='bottom', color=BL)
    wire(d, (1.8, 3.4), (3.2, 3.4))
    el(d, E.Resistor, (3.2, 3.4), (6.2, 3.4), '4Ω')
    wire(d, (3.2, 3.4), (3.2, 2.0))
    d += E.Capacitor().endpoints((3.2, 2.0), (6.2, 2.0)).label(('+', 'v_C', '−'), loc='bottom').label('2F').color(HL)
    wire(d, (6.2, 2.0), (6.2, 3.4), (8.2, 3.4))
    el(d, E.Capacitor, (6.2, 2.0), (6.2, 0), '4F', loc='bottom')
    el(d, E.Resistor, (8.2, 3.4), (8.2, 1.7), '8Ω', loc='bottom')
    el(d, E.Capacitor, (8.2, 1.7), (8.2, 0), ('+', '1F  e', '−'), loc='bottom')
    wire(d, (0, 0), (8.2, 0))
    dot(d, (1.8, 3.4), (3.2, 3.4), (6.2, 3.4), (6.2, 2.0), (1.8, 0), (6.2, 0))
    text(d, 1.8, 3.85, 'M', color=BL)
    text(d, 6.2, 3.85, 'N', color=BL)
    return d
