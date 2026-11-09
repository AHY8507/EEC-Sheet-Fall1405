from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, box


def src_r(d, label='Vs', r='R'):
    el(d, E.SourceV, (0, 0), (0, 3), label)
    el(d, E.Resistor, (0, 3), (3, 3), r)


@ckt('b10-four')
def _():
    d = new(unit=2.2, fontsize=12)
    # capacitive loop: two parallel caps
    el(d, E.Capacitor, (0, 0), (0, 2.4), 'C₁', color=HL)
    el(d, E.Capacitor, (1.8, 0), (1.8, 2.4), 'C₂', loc='bottom', color=HL)
    wire(d, (0, 2.4), (1.8, 2.4)); wire(d, (0, 0), (1.8, 0))
    text(d, 0.9, -0.7, 'حلقه خازنی ✓')
    # inductive cutset: two series inductors
    o = 3.6
    el(d, E.Inductor2, (o, 1.2), (o + 2, 1.2), 'L₁', loops=2, color=HL)
    el(d, E.Inductor2, (o + 2, 1.2), (o + 4, 1.2), 'L₂', loops=2, color=HL)
    dot(d, (o + 2, 1.2))
    text(d, o + 2, -0.7, 'کات‌ست سلفی ✓')
    # capacitive cutset: series caps
    o = 9.0
    el(d, E.Capacitor, (o, 1.2), (o + 2, 1.2), 'C₁')
    el(d, E.Capacitor, (o + 2, 1.2), (o + 4, 1.2), 'C₂')
    dot(d, (o + 2, 1.2))
    text(d, o + 2, -0.7, 'کات‌ست خازنی ✗')
    # inductive loop: parallel inductors
    o = 14.4
    el(d, E.Inductor2, (o, 0), (o, 2.4), 'L₁', loops=2)
    el(d, E.Inductor2, (o + 1.8, 0), (o + 1.8, 2.4), 'L₂', loc='bottom', loops=2)
    wire(d, (o, 2.4), (o + 1.8, 2.4)); wire(d, (o, 0), (o + 1.8, 0))
    text(d, o + 0.9, -0.7, 'حلقه سلفی ✗')
    return d


@ckt('b10-parc')
def _():
    d = new()
    src_r(d)
    el(d, E.Capacitor, (3, 3), (3, 0), 'C₁', loc='bottom')
    wire(d, (3, 3), (5.5, 3))
    el(d, E.Capacitor, (5.5, 3), (5.5, 0), 'C₂', loc='bottom')
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    box(d, 2.2, -0.4, 6.6, 3.4, color=HL, dash=True)
    return d


@ckt('b10-csrc')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'Vs')
    wire(d, (0, 3), (2.5, 3))
    el(d, E.Capacitor, (2.5, 3), (2.5, 0), 'C₁', loc='bottom')
    el(d, E.Resistor, (2.5, 3), (5.5, 3), 'R')
    el(d, E.Capacitor, (5.5, 3), (5.5, 0), 'C₂', loc='bottom')
    wire(d, (0, 0), (5.5, 0))
    dot(d, (2.5, 3), (2.5, 0))
    box(d, -1.5, -0.4, 3.3, 3.4, color=HL, dash=True)
    return d


@ckt('b10-serl')
def _():
    d = new()
    src_r(d)
    el(d, E.Inductor2, (3, 3), (3, 0), 'L₁', loc='bottom', loops=3)
    el(d, E.Inductor2, (3, 0), (0, 0), 'L₂', loops=3)
    dot(d, (3, 0))
    box(d, 2.5, -0.5, 3.5, 0.5, color=HL, dash=True)
    return d


@ckt('b10-lisrc')
def _():
    d = new()
    el(d, E.SourceI, (0, 0), (0, 3), 'Is')
    el(d, E.Inductor2, (0, 3), (3, 3), 'L₁', loops=3)
    dot(d, (0, 3))
    box(d, -0.5, 2.5, 0.5, 3.5, color=HL, dash=True)
    el(d, E.Resistor, (3, 3), (3, 0), 'R', loc='bottom')
    wire(d, (3, 3), (5.5, 3))
    el(d, E.Inductor2, (5.5, 3), (5.5, 0), 'L₂', loc='bottom', loops=3)
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    text(d, 3, 3.5, 'a')
    return d


@ckt('b10-delta')
def _():
    d = new()
    src_r(d, r='R₁')
    el(d, E.Capacitor, (3, 3), (3, 0), 'C₁', loc='bottom', color=HL)
    el(d, E.Capacitor, (3, 3), (6, 3), 'C₂', color=HL)
    el(d, E.Capacitor, (6, 3), (6, 0), 'C₃', loc='bottom', color=HL)
    wire(d, (6, 3), (8.5, 3))
    el(d, E.Resistor, (8.5, 3), (8.5, 0), 'R₂', loc='bottom')
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3, 3), (6, 3), (3, 0), (6, 0))
    text(d, 3, 3.5, 'a'); text(d, 6, 3.5, 'b')
    return d


@ckt('b10-both')
def _():
    d = new()
    src_r(d, r='R₁')
    el(d, E.Capacitor, (3, 3), (3, 0), 'C₁', loc='bottom', color=HL)
    wire(d, (3, 3), (5, 3))
    el(d, E.Capacitor, (5, 3), (5, 0), 'C₂', loc='bottom', color=HL)
    el(d, E.Inductor2, (5, 3), (7.5, 3), 'L₁', loops=3, color=BL)
    el(d, E.Inductor2, (7.5, 3), (10, 3), 'L₂', loops=3, color=BL)
    el(d, E.Capacitor, (10, 3), (10, 0), 'C₃', loc='bottom')
    wire(d, (10, 3), (12, 3))
    el(d, E.Resistor, (12, 3), (12, 0), 'R₂', loc='bottom')
    wire(d, (0, 0), (12, 0))
    dot(d, (3, 3), (5, 3), (7.5, 3), (10, 3), (3, 0), (5, 0), (10, 0))
    text(d, 3, 3.5, 'a'); text(d, 7.5, 3.6, 'b'); text(d, 10, 3.5, 'c')
    return d


@ckt('b10-serc')
def _():
    d = new()
    src_r(d)
    el(d, E.Capacitor, (3, 3), (3, 0), 'C₁', loc='bottom')
    el(d, E.Capacitor, (3, 0), (0, 0), 'C₂')
    dot(d, (3, 0))
    return d


@ckt('b10-parl')
def _():
    d = new()
    src_r(d)
    el(d, E.Inductor2, (3, 3), (3, 0), 'L₁', loc='bottom', loops=3)
    wire(d, (3, 3), (5.5, 3))
    el(d, E.Inductor2, (5.5, 3), (5.5, 0), 'L₂', loc='bottom', loops=3)
    wire(d, (0, 0), (5.5, 0))
    dot(d, (3, 3), (3, 0))
    return d


@ckt('b10-tricky')
def _():
    d = new()
    el(d, E.SourceV, (0, 0), (0, 3), 'Vs')
    el(d, E.Inductor2, (0, 3), (3, 3), 'L₁', loops=3)
    el(d, E.Capacitor, (3, 3), (3, 0), 'C', loc='bottom')
    el(d, E.Inductor2, (3, 3), (6, 3), 'L₂', loops=3)
    el(d, E.Resistor, (6, 3), (6, 0), 'R', loc='bottom', color=HL)
    wire(d, (6, 3), (8.5, 3))
    el(d, E.SourceI, (8.5, 0), (8.5, 3), 'I', loc='bottom')
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3, 3), (6, 3), (3, 0), (6, 0))
    text(d, 3, 3.5, 'a'); text(d, 6, 3.5, 'b')
    return d
