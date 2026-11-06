from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, box


@ckt('b4-ladder')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'Vs')
    el(d, E.Resistor, (0, 3), (3, 3), '1Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '2Ω', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '1Ω')
    el(d, E.Resistor, (6, 3), (6, 0), ('+', '1Ω   v_out', '−'), loc='bottom', color=HL)
    wire(d, (0, 0), (6, 0))
    dot(d, (3, 3), (3, 0))
    text(d, 3, 3.5, 'a')
    text(d, 6, 3.5, 'b')
    return d


@ckt('b4-sp')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (3, 3), '3Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '6Ω', loc='bottom')
    wire(d, (3, 3), (5.5, 3))
    el(d, E.SourceI, (5.5, 0), (5.5, 3), '2A', loc='bottom')
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    text(d, 3, 3.5, 'a')
    return d


@ckt('b4-sp3')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '10V')
    R = el(d, E.Resistor, (0, 3), (3, 3), '2Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('i₁')
    el(d, E.Resistor, (3, 3), (3, 0), '4Ω', loc='bottom')
    wire(d, (3, 3), (5.5, 3))
    el(d, E.SourceI, (5.5, 0), (5.5, 3), '3A', loc='bottom')
    wire(d, (5.5, 3), (8, 3))
    el(d, E.SourceControlledI, (8, 0), (8, 3), '0.5 i₁', loc='bottom', color=HL)
    wire(d, (0, 0), (8, 0))
    dot(d, (3, 3), (5.5, 3), (3, 0), (5.5, 0))
    text(d, 3, 3.5, 'a')
    return d


@ckt('b4-th1')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    el(d, E.Resistor, (0, 3), (3, 3), '4Ω')
    el(d, E.Resistor, (3, 3), (3, 0), '12Ω', loc='bottom')
    el(d, E.Resistor, (3, 3), (6, 3), '2Ω')
    wire(d, (0, 0), (6, 0))
    dot(d, (3, 3), (3, 0))
    dot(d, (6, 3), open=True, lab='a', loc='right')
    dot(d, (6, 0), open=True, lab='b', loc='right')
    el(d, E.Resistor, (7.5, 3), (7.5, 0), 'R_L', loc='bottom', color=MU)
    wire(d, (6.15, 3), (7.5, 3), color=MU)
    wire(d, (6.15, 0), (7.5, 0), color=MU)
    return d


@ckt('b4-models')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'V_th')
    el(d, E.Resistor, (0, 3), (3, 3), 'R_th')
    wire(d, (0, 0), (3, 0))
    dot(d, (3, 3), open=True, lab='a', loc='right')
    dot(d, (3, 0), open=True, lab='b', loc='right')
    text(d, 1.5, -0.8, 'معادل تونن')
    text(d, 4.6, 1.5, '⟺')
    el(d, E.SourceI, (6.5, 0), (6.5, 3), 'I_N', loc='bottom')
    wire(d, (6.5, 3), (10, 3))
    wire(d, (6.5, 0), (10, 0))
    el(d, E.Resistor, (8.3, 3), (8.3, 0), 'R_N = R_th', loc='bottom')
    dot(d, (8.3, 3), (8.3, 0))
    dot(d, (10, 3), open=True, lab='a', loc='right')
    dot(d, (10, 0), open=True, lab='b', loc='right')
    text(d, 8.3, -0.8, 'معادل نورتن')
    return d


@ckt('b4-proof')
def _():
    d = new()
    box(d, 0, -0.4, 3.2, 3.4, 'مدار خطی')
    wire(d, (3.2, 3), (5, 3))
    wire(d, (3.2, 0), (5, 0))
    dot(d, (5, 3), open=True, lab='a', loc='top')
    dot(d, (5, 0), open=True, lab='b', loc='bottom')
    el(d, E.SourceI, (6.8, 3), (6.8, 0), 'i (آزمون)', loc='bottom', color=HL)
    wire(d, (5.1, 3), (6.8, 3))
    wire(d, (5.1, 0), (6.8, 0))
    text(d, 4.6, 2.6, '+')
    text(d, 4.6, 1.5, 'v')
    text(d, 4.6, 0.4, '−')
    return d


@ckt('b4-thdep')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), '12V')
    R = el(d, E.Resistor, (0, 3), (3, 3), '3Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('i₁')
    el(d, E.Resistor, (3, 3), (3, 0), '6Ω', loc='bottom')
    wire(d, (3, 3), (5.5, 3))
    el(d, E.SourceControlledI, (5.5, 3), (5.5, 0), '0.5 i₁', loc='bottom', color=HL)
    wire(d, (0, 0), (5.5, 0))
    wire(d, (5.5, 3), (7, 3))
    wire(d, (5.5, 0), (7, 0))
    dot(d, (3, 3), (5.5, 3), (3, 0), (5.5, 0))
    dot(d, (7, 3), open=True, lab='a', loc='right')
    dot(d, (7, 0), open=True, lab='b', loc='right')
    return d


@ckt('b4-noind')
def _():
    d = new()
    dot(d, (0, 3), open=True, lab='a', loc='left')
    dot(d, (0, 0), open=True, lab='b', loc='left')
    R = el(d, E.Resistor, (0, 3), (3, 3), '2Ω')
    d += E.CurrentLabelInline(direction='in').at(R).label('i')
    el(d, E.SourceControlledV, (3, 0), (3, 3), 'k·i', loc='bottom', color=HL)
    wire(d, (0, 0), (3, 0))
    return d
