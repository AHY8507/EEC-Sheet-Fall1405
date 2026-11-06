from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


def opamp(d, at=(0, 0)):
    op = E.Opamp(leads=True).at(at).anchor('center')
    d += op
    return op


@ckt('b11-rc0')
def _():
    d = new()
    el(d, E.Capacitor, (0, 0), (0, 3), ('−', 'C', '+'))
    R = el(d, E.Resistor, (0, 3), (3, 3), 'R')
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    wire(d, (3, 3), (3, 0), (0, 0))
    text(d, -1.2, 3.3, 'v(0) = V₀')
    return d


@ckt('b11-rl0')
def _():
    d = new()
    L = el(d, E.Inductor2, (0, 0), (0, 3), 'L', loops=3)
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=True, reverse=True).at(L).label('i_L')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    wire(d, (3, 3), (3, 0), (0, 0))
    return d


@ckt('b11-rcs')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'Vs')
    el(d, E.Resistor, (0, 3), (3, 3), 'R')
    el(d, E.Capacitor, (3, 3), (3, 0), ('+', 'C   v_C', '−'), loc='bottom')
    wire(d, (0, 0), (3, 0))
    return d


@ckt('b11-ex1')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '20V')
    el(d, E.Resistor, (0, 3), (3, 3), '10k')
    el(d, E.Switch, (3, 3), (5.4, 3), 't = 0', action='close', color=HL)
    el(d, E.Capacitor, (5.4, 3), (5.4, 0), ('+', '50µF', '−'), loc='bottom')
    wire(d, (5.4, 3), (8, 3))
    el(d, E.Resistor, (8, 3), (8, 0), '40k', loc='bottom')
    wire(d, (0, 0), (8, 0))
    dot(d, (5.4, 3), (5.4, 0))
    return d


@ckt('b11-ex2')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), '6A')
    wire(d, (0, 3), (2.6, 3))
    el(d, E.Resistor, (2.6, 3), (2.6, 0), '3Ω', loc='bottom')
    el(d, E.Switch, (2.6, 3), (5.2, 3), 't = 0', action='open', color=HL)
    L = el(d, E.Inductor2, (5.2, 3), (5.2, 0), '0.6H', loc='bottom', loops=3)
    d += E.CurrentLabel(ofst=0.5, length=1.0, top=False).at(L).label('i_L')
    wire(d, (5.2, 3), (7.8, 3))
    el(d, E.Resistor, (7.8, 3), (7.8, 0), '6Ω', loc='bottom')
    wire(d, (0, 0), (7.8, 0))
    dot(d, (2.6, 3), (5.2, 3), (2.6, 0), (5.2, 0))
    return d


@ckt('b11-ex3')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'v_s(t)', color=HL)
    el(d, E.Resistor, (0, 3), (3, 3), '4Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '12Ω', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '2Ω')
    el(d, E.Capacitor, (6, 3), (6, 0), ('+', '0.1F  v_C', '−'), loc='bottom')
    wire(d, (0, 0), (6, 0))
    dot(d, (3, 3), (3, 0))
    text(d, 3, 3.5, 'm')
    return d


@ckt('b11-integ')
def _():
    d = new()
    op = opamp(d, (0, 0))
    wire(d, op.in2, (op.in2[0], op.in2[1] - 0.6))
    gnd(d, (op.in2[0], op.in2[1] - 0.6))
    dot(d, op.in1)
    el(d, E.Resistor, (op.in1[0] - 3, op.in1[1]), op.in1, 'R')
    dot(d, (op.in1[0] - 3, op.in1[1]), open=True, lab='v_i', loc='left')
    wire(d, op.in1, (op.in1[0], op.in1[1] + 1.6))
    el(d, E.Capacitor, (op.in1[0], op.in1[1] + 1.6), (op.out[0], op.in1[1] + 1.6), 'C', color=HL)
    wire(d, (op.out[0], op.in1[1] + 1.6), op.out)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d


@ckt('b11-diff')
def _():
    d = new()
    op = opamp(d, (0, 0))
    wire(d, op.in2, (op.in2[0], op.in2[1] - 0.6))
    gnd(d, (op.in2[0], op.in2[1] - 0.6))
    dot(d, op.in1)
    el(d, E.Capacitor, (op.in1[0] - 3, op.in1[1]), op.in1, 'C', color=HL)
    dot(d, (op.in1[0] - 3, op.in1[1]), open=True, lab='v_i', loc='left')
    wire(d, op.in1, (op.in1[0], op.in1[1] + 1.6))
    el(d, E.Resistor, (op.in1[0], op.in1[1] + 1.6), (op.out[0], op.in1[1] + 1.6), 'R')
    wire(d, (op.out[0], op.in1[1] + 1.6), op.out)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d


@ckt('b11-dep')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10u(t)')
    R = el(d, E.Resistor, (0, 3), (3, 3), '2Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('iₓ')
    el(d, E.Capacitor, (3, 3), (3, 0), ('+', '0.5F', '−'), loc='bottom')
    wire(d, (3, 3), (5.5, 3))
    el(d, E.SourceControlledI, (5.5, 3), (5.5, 0), '0.5 iₓ', loc='bottom', color=HL)
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    return d
