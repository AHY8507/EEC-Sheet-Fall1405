from ck import ckt, new, E, HL, BL, MU, el, wire, dot, gnd, text, npass, ppass, tg, nfet


@ckt('c4-npass')
def _():
    d = new()
    dot(d, (0, 0), open=True, lab='V_in', loc='left')
    npass(d, (0, 0), color=HL, gate='V_DD')
    wire(d, (1.5, 0), (3, 0))
    dot(d, (3, 0))
    el(d, E.Capacitor, (3, 0), (3, -2), 'C', loc='bottom')
    gnd(d, (3, -2))
    wire(d, (3, 0), (4.2, 0))
    dot(d, (4.2, 0), open=True, lab='V_out', loc='right')
    return d


@ckt('c4-series')
def _():
    d = new(fontsize=12)
    dot(d, (0, 0), open=True, lab='V_DD', loc='left')
    x = 0
    for k in range(3):
        npass(d, (x, 0), gate='V_DD')
        x += 1.5
        if k < 2:
            wire(d, (x, 0), (x + 0.6, 0))
            x += 0.6
    dot(d, (x, 0), open=True, lab='V_DD − V_th', loc='right')
    return d


@ckt('c4-g2o')
def _():
    d = new(fontsize=12)
    wire(d, (-0.5, 3.0), (9.5, 3.0))
    text(d, -1.3, 3.0, 'V_DD')
    xs = [1.5, 4.8, 8.1]
    prev = None
    labs = ['V_DD − V_th', 'V_DD − 2V_th', 'V_DD − 3V_th']
    for k, x in enumerate(xs):
        q = nfet(d, (x, 0))
        wire(d, q.drain, (x, 3.0))
        dot(d, (x, 3.0))
        if prev is None:
            wire(d, q.gate, (q.gate[0] - 0.8, q.gate[1]), (q.gate[0] - 0.8, 3.0))
            dot(d, (q.gate[0] - 0.8, 3.0))
        else:
            wire(d, prev, (prev[0], -0.6), (q.gate[0] - 0.8, -0.6), (q.gate[0] - 0.8, q.gate[1]), q.gate)
        el(d, E.Capacitor, q.source, (x, -1.8), '', loc='bottom', color=MU)
        gnd(d, (x, -1.8))
        dot(d, q.source)
        text(d, x + 1.35, -1.15, labs[k], color=HL)
        prev = q.source
    return d


@ckt('c4-tg')
def _():
    d = new(fontsize=12)
    dot(d, (0, 0), open=True, lab='in', loc='left')
    tg(d, (0, 0), 'S', color=HL)
    dot(d, (2.5, 0), open=True, lab='out', loc='right')
    return d


@ckt('c4-mux')
def _():
    d = new(fontsize=12)
    dot(d, (0, 2.6), open=True, lab='A', loc='left')
    tg(d, (0, 2.6), 'S', color=HL)
    dot(d, (0, -2.6), open=True, lab='B', loc='left')
    tg(d, (0, -2.6), 'S̅', color=BL)
    wire(d, (2.5, 2.6), (3.3, 2.6), (3.3, -2.6), (2.5, -2.6))
    dot(d, (3.3, 0))
    wire(d, (3.3, 0), (4.3, 0))
    dot(d, (4.3, 0), open=True, lab='F = A·S + B·S̅', loc='right')
    return d
