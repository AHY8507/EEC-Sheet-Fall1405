"""Circuits for the section on jumps of v_C and i_L (chapter B12)."""
from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


@ckt('b12-j-c')
def _():
    """Two capacitors suddenly connected in parallel (all-capacitor loop); R only discharges afterwards."""
    d = new()
    el(d, E.Capacitor, (0, 0), (0, 3), ('−', 'C₁ = 1mF (5V)', '+'))
    el(d, E.Switch, (0, 3), (3.2, 3), 't = 0', action='close', color=HL)
    el(d, E.Capacitor, (3.2, 0), (3.2, 3), ('−', 'C₂ = 1mF (0V)', '+'), loc='bottom')
    wire(d, (3.2, 3), (8.6, 3))
    el(d, E.Resistor, (8.6, 3), (8.6, 0), '1kΩ', loc='bottom')
    wire(d, (0, 0), (8.6, 0))
    dot(d, (3.2, 3), (3.2, 0))
    return d


@ckt('b12-j-cv')
def _():
    """A charged capacitor connected straight to an ideal voltage source."""
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10V')
    el(d, E.Switch, (0, 3), (3, 3), 't = 0', action='close', color=HL)
    el(d, E.Capacitor, (3, 3), (3, 0), ('+', 'C = 2µF   v_C(0⁻) = 2V', '−'), loc='bottom')
    wire(d, (0, 0), (3, 0))
    return d


@ckt('b12-j-l')
def _():
    """Two inductors with different currents forced into one series loop with R."""
    d = new()
    wire(d, (0, 3), (0, 0))
    wire(d, (0, 0), (5.8, 0))
    el(d, E.Inductor2, (0, 3), (2.9, 3), 'L₁ = 2H', loc='bottom', loops=3)
    el(d, E.Inductor2, (2.9, 3), (5.8, 3), 'L₂ = 2H', loc='bottom', loops=3)
    el(d, E.Resistor, (5.8, 3), (5.8, 0), '3Ω', loc='bottom')
    # the switches that keep each inductor in its own short-circuited loop until t = 0
    wire(d, (0, 3), (0, 4.4))
    el(d, E.Switch, (0, 4.4), (2.9, 4.4), 't = 0', action='open', color=HL)
    wire(d, (2.9, 4.4), (2.9, 3))
    wire(d, (2.9, 3), (2.9, 4.4))
    el(d, E.Switch, (2.9, 4.4), (5.8, 4.4), 't = 0', action='open', color=HL)
    wire(d, (5.8, 4.4), (5.8, 3))
    dot(d, (0, 3), (2.9, 3), (5.8, 3))
    text(d, 1.45, 1.2, 'i₁(0⁻) = 4A', color=MU)
    text(d, 3.9, 1.2, 'i₂(0⁻) = 0', color=MU)
    return d


@ckt('b12-j-li')
def _():
    """An inductor with its own current suddenly placed in series with an ideal current source."""
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '3A')
    wire(d, (0, 3), (1, 3))
    el(d, E.Inductor2, (1, 3), (4, 3), 'L = 0.5H', loc='bottom', loops=3)
    wire(d, (4, 3), (5, 3))
    wire(d, (5, 3), (5, 0))
    wire(d, (5, 0), (0, 0))
    wire(d, (1, 3), (1, 4.4))
    el(d, E.Switch, (1, 4.4), (4, 4.4), 't = 0', action='open', color=HL)
    wire(d, (4, 4.4), (4, 3))
    dot(d, (1, 3), (4, 3))
    text(d, 2.5, 1.6, 'i_L(0⁻) = 1A', color=MU)
    return d


@ckt('b12-j-rlc')
def _():
    """Jump of v_C followed by a second-order response: C1 is switched across C2, which sits in a series RL loop."""
    d = new()
    el(d, E.Capacitor, (0, 0), (0, 3), ('−', 'C₁ = 1F (6V)', '+'))
    el(d, E.Switch, (0, 3), (3, 3), 't = 0', action='close', color=HL)
    el(d, E.Capacitor, (3, 0), (3, 3), ('−', 'C₂ = 1F (0V)', '+'), loc='bottom')
    wire(d, (3, 3), (4.4, 3))
    el(d, E.Resistor, (4.4, 3), (7.4, 3), '1Ω')
    L = el(d, E.Inductor2, (7.4, 3), (7.4, 0), '0.5H', loc='bottom', loops=3)
    wire(d, (0, 0), (7.4, 0))
    dot(d, (3, 3), (3, 0))
    return d
