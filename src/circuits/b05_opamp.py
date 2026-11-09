from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text


def opamp(d, at=(0, 0)):
    """Op-amp with inverting input on top (in1) and non-inverting at bottom (in2)."""
    op = E.Opamp(leads=True).at(at).anchor('center')
    d += op
    return op


@ckt('b5-model')
def _():
    d = new(fontsize=12)
    op = opamp(d, (0, 0))
    text(d, op.in1[0] - 0.4, op.in1[1] + 0.4, 'v₋')
    text(d, op.in2[0] - 0.4, op.in2[1] - 0.45, 'v₊')
    text(d, op.out[0] + 0.5, op.out[1] + 0.4, 'v_o')
    # equivalent model to the right
    x0 = 5
    dot(d, (x0, 1), open=True, lab='v₋', loc='left')
    dot(d, (x0, -1), open=True, lab='v₊', loc='left')
    el(d, E.Resistor, (x0 + 1.4, 1), (x0 + 1.4, -1), 'R_in', loc='bottom')
    wire(d, (x0, 1), (x0 + 1.4, 1))
    wire(d, (x0, -1), (x0 + 1.4, -1))
    el(d, E.SourceControlledV, (x0 + 3.6, -1.6), (x0 + 3.6, 1.2), 'A(v₊ − v₋)', loc='bottom', color=HL)
    el(d, E.Resistor, (x0 + 3.6, 1.2), (x0 + 7.4, 1.2), 'R_out')
    dot(d, (x0 + 7.4, 1.2), open=True, lab='v_o', loc='right')
    gnd(d, (x0 + 3.6, -1.6))
    return d


@ckt('b5-inv')
def _():
    d = new()
    op = opamp(d, (0, 0))
    wire(d, op.in2, (op.in2[0], op.in2[1] - 0.6))
    gnd(d, (op.in2[0], op.in2[1] - 0.6))
    dot(d, op.in1)
    el(d, E.Resistor, (op.in1[0] - 3, op.in1[1]), op.in1, 'R₁')
    dot(d, (op.in1[0] - 3, op.in1[1]), open=True, lab='v_i', loc='left')
    wire(d, op.in1, (op.in1[0], op.in1[1] + 1.6))
    el(d, E.Resistor, (op.in1[0], op.in1[1] + 1.6), (op.out[0], op.in1[1] + 1.6), 'R_f', color=HL)
    wire(d, (op.out[0], op.in1[1] + 1.6), op.out)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d


@ckt('b5-noninv')
def _():
    d = new()
    op = opamp(d, (0, 0))
    wire(d, op.in2, (op.in2[0] - 1.6, op.in2[1]))
    dot(d, (op.in2[0] - 1.6, op.in2[1]), open=True, lab='v_i', loc='left')
    dot(d, op.in1)
    el(d, E.Resistor, op.in1, (op.in1[0] - 2.4, op.in1[1]), 'R₁', loc='bottom')
    gnd(d, (op.in1[0] - 2.4, op.in1[1]))
    wire(d, op.in1, (op.in1[0], op.in1[1] + 1.6))
    el(d, E.Resistor, (op.in1[0], op.in1[1] + 1.6), (op.out[0], op.in1[1] + 1.6), 'R_f', color=HL)
    wire(d, (op.out[0], op.in1[1] + 1.6), op.out)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d


@ckt('b5-follower')
def _():
    d = new()
    op = opamp(d, (0, 0))
    wire(d, op.in2, (op.in2[0] - 1.6, op.in2[1]))
    dot(d, (op.in2[0] - 1.6, op.in2[1]), open=True, lab='v_i', loc='left')
    wire(d, op.in1, (op.in1[0], op.in1[1] + 1.4), (op.out[0], op.in1[1] + 1.4), op.out, color=HL)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d


@ckt('b5-sum')
def _():
    d = new()
    op = opamp(d, (0, 0))
    wire(d, op.in2, (op.in2[0], op.in2[1] - 0.6))
    gnd(d, (op.in2[0], op.in2[1] - 0.6))
    n = (op.in1[0] - 1.0, op.in1[1])
    wire(d, n, op.in1)
    dot(d, n)
    for k, (y, lab) in enumerate(((2.2, 'R₁'), (0.5, 'R₂'), (-1.2, 'R₃'))):
        p = (n[0] - 3, n[1] + y - 0.5)
        el(d, E.Resistor, p, (n[0] - 0.6, p[1]), lab)
        wire(d, (n[0] - 0.6, p[1]), (n[0], p[1]))
        dot(d, p, open=True, lab='v%s' % '₁₂₃'[k], loc='left')
    wire(d, (n[0], n[1] + 1.7), (n[0], n[1] - 1.7))
    wire(d, (n[0], n[1] + 1.7), (n[0], n[1] + 2.6))
    el(d, E.Resistor, (n[0], n[1] + 2.6), (op.out[0], n[1] + 2.6), 'R_f', color=HL)
    wire(d, (op.out[0], n[1] + 2.6), op.out)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d


@ckt('b5-diff')
def _():
    d = new()
    op = opamp(d, (0, 0))
    dot(d, op.in1, op.in2)
    el(d, E.Resistor, (op.in1[0] - 3, op.in1[1]), op.in1, 'R₁')
    dot(d, (op.in1[0] - 3, op.in1[1]), open=True, lab='v₁', loc='left')
    el(d, E.Resistor, (op.in2[0] - 3, op.in2[1]), op.in2, 'R₃', loc='bottom')
    dot(d, (op.in2[0] - 3, op.in2[1]), open=True, lab='v₂', loc='left')
    el(d, E.Resistor, op.in2, (op.in2[0], op.in2[1] - 2.6), 'R₄', loc='bottom')
    gnd(d, (op.in2[0], op.in2[1] - 2.6))
    wire(d, op.in1, (op.in1[0], op.in1[1] + 1.6))
    el(d, E.Resistor, (op.in1[0], op.in1[1] + 1.6), (op.out[0], op.in1[1] + 1.6), 'R₂', color=HL)
    wire(d, (op.out[0], op.in1[1] + 1.6), op.out)
    dot(d, op.out)
    wire(d, op.out, (op.out[0] + 1.2, op.out[1]))
    dot(d, (op.out[0] + 1.2, op.out[1]), open=True, lab='v_o', loc='right')
    return d
