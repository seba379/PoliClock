"""Coppia USB D+/D- tracciata a mano (DEC-041), piste bloccate: Freerouting non le tocca.

Geometria, vista dall'alto, asse a = centro dei contatti D del connettore = centro dei pin 26/27 del modulo
(J1, U1, R3/R4 e pin del modulo sono allineati sullo stesso asse in posizioni_main.py):

  connettore J1 (contatti a passo 0,5 mm): B7 D-  A6 D+  A7 D-  B6 D+  (u = -0,75 -0,25 +0,25 +0,75)
  - percorso principale, senza vie e simmetrico rispetto all'asse: B7 (D-) a sinistra e B6 (D+) a destra,
    nello stesso ordine dei pin del modulo (26 = D- a sinistra, 27 = D+ a destra);
  - i contatti interni A6/A7 (l'altra faccia della spina) si incrociano: ciascuno sale sul lato superiore,
    passa sul retro con una via, attraversa e risale con una seconda via sulla propria linea.
    Due vie per rete (stesso numero su D+ e D-). Le due vie di D- stanno 0,8 mm piu' in alto di quelle di D+
    e il ramo superiore di A7 e' piu' lungo di 0,8 mm: i percorsi completi contatto -> pin del modulo restano
    uguali su entrambe le facce della spina (vedi lunghezze stampate).
  - USBLC6 (U1) a passaggio diretto: D- sui pin 1/6, D+ sui pin 3/4; GND (pin 2) verso il connettore con una
    via al piano; +5V (pin 5) verso il modulo, esce sotto il corpo di R4 (0 ohm) fra le sue piazzole, senza vie.
  - R4/R3 (0 ohm) simmetrici, poi la coppia converge sui pin 26/27 del modulo.
Sul retro, sotto la coppia fra U1 e il modulo, una zona vietata a piste e vie lascia il piano GND continuo.
"""
import math
import pcbnew

MM = pcbnew.FromMM
W_D = 0.2        # larghezza delle piste D+/D- (mm)
W_5V = 0.3       # pista +5V verso il pin VBUS dell'USBLC6
VIA = (0.6, 0.3)


def _pad(fps, ref, num):
    p = [p for p in fps[ref].Pads() if p.GetNumber() == num][0]
    return pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y), p


def _len(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def traccia(board, fps, OX, OY):
    """Disegna la coppia; restituisce (rettangolo zona retro in coordinate scheda, dizionario lunghezze)."""
    nets = {n: board.FindNet(n) for n in ("USB_DN_C", "USB_DP_C", "USB_DN", "USB_DP", "+5V", "GND")}
    nets = {k: (v if v else board.FindNet("/USB e alimentazione/" + k)) for k, v in nets.items()}
    for k, v in nets.items():
        assert v, k

    def seg(pts, net, w, layer=pcbnew.F_Cu):
        for a, b in zip(pts, pts[1:]):
            if math.dist(a, b) < 1e-6:
                continue
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1])))
            t.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1])))
            t.SetWidth(MM(w))
            t.SetLayer(layer)
            t.SetNet(nets[net])
            t.SetLocked(True)
            board.Add(t)

    def via(p, net):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(MM(p[0]), MM(p[1])))
        v.SetWidth(MM(VIA[0]))
        v.SetDrill(MM(VIA[1]))
        v.SetNet(nets[net])
        v.SetLocked(True)
        board.Add(v)

    b7x, P, _ = _pad(fps, "J1", "B7")
    b6x, _, _ = _pad(fps, "J1", "B6")
    a = (b7x + b6x) / 2
    m26x, Q, _ = _pad(fps, "U3", "26")
    m27x, _, _ = _pad(fps, "U3", "27")
    assert abs((m26x + m27x) / 2 - a) < 0.03, "connettore e pin USB del modulo non allineati"
    u1 = {n: _pad(fps, "U1", n)[:2] for n in "123456"}
    r4 = {n: _pad(fps, "R4", n)[:2] for n in "12"}
    r3 = {n: _pad(fps, "R3", n)[:2] for n in "12"}
    assert u1["1"][0] < a < u1["3"][0] and u1["1"][1] > u1["6"][1], "orientamento U1 inatteso"

    X = lambda u: a + u  # noqa: E731
    yF = P - 1.78        # fine del tratto dritto dai contatti
    yW = P - 2.23        # linee principali allargate a +-1,2 mm
    yV1 = P - 2.68       # vie di D+ (A6 -> linea D+)
    yV2 = P - 3.48       # vie di D- (A7 -> linea D-), 0,8 mm piu' in alto
    yC = P - 3.68        # inizio convergenza verso i pin di U1
    yU = u1["1"][1]      # riga dei pin 1/2/3 di U1 (verso il connettore)
    uU = u1["3"][0] - a  # +0,95: colonna dei pin D+ di U1

    # percorsi principali (contatti B7/B6 -> U1 -> R -> modulo), speculari
    def principale(s, pin_u_low, pin_u_high, r, pin_m):
        # i punti delle vie dell'incrocio sono vertici della pista (Freerouting collega solo agli estremi)
        return [(X(s * 0.75), P), (X(s * 0.75), yF), (X(s * 1.2), yW), (X(s * 1.2), yV1), (X(s * 1.2), yV2),
                (X(s * 1.2), yC),
                (X(s * uU), yC - 0.25), pin_u_low, pin_u_high, r["1"], r["2"],
                (r["2"][0], Q + 1.435), (pin_m[0], Q + 0.885), pin_m]
    dn = principale(-1, u1["1"], u1["6"], r4, (m26x, Q))
    dp = principale(+1, u1["3"], u1["4"], r3, (m27x, Q))
    # indici: 0..9 contatto -> U1 -> piazzola 1 di R (rete *_C), 10.. piazzola 2 di R -> modulo; R non va cortocircuitata
    seg(dn[:10], "USB_DN_C", W_D)
    seg(dn[10:], "USB_DN", W_D)
    seg(dp[:10], "USB_DP_C", W_D)
    seg(dp[10:], "USB_DP", W_D)

    # rami dei contatti interni con l'incrocio sul retro
    a6 = [(X(-0.25), P), (X(-0.25), yW + 0.15), (X(-0.4), yW), (X(-0.4), yV1)]
    a7 = [(X(0.25), P), (X(0.25), yW + 0.15), (X(0.4), yW), (X(0.4), yV2)]
    seg(a6, "USB_DP_C", W_D)
    seg(a7, "USB_DN_C", W_D)
    via(a6[-1], "USB_DP_C")
    via((X(1.2), yV1), "USB_DP_C")
    seg([a6[-1], (X(1.2), yV1)], "USB_DP_C", W_D, pcbnew.B_Cu)
    via(a7[-1], "USB_DN_C")
    via((X(-1.2), yV2), "USB_DN_C")
    seg([a7[-1], (X(-1.2), yV2)], "USB_DN_C", W_D, pcbnew.B_Cu)

    # U1: GND (pin 2) al piano con una via; +5V (pin 5) sotto il corpo di R4
    g = (X(-0.3), yU + 1.06)
    seg([u1["2"], (u1["2"][0], yU + 0.66), g], "GND", 0.3)
    via(g, "GND")
    yr = (r4["1"][1] + r4["2"][1]) / 2
    seg([u1["5"], (u1["5"][0], yr), (X(-2.4), yr)], "+5V", W_5V)

    # lunghezze dei percorsi completi contatto -> pin del modulo (le vie contano come 1,6 mm ciascuna)
    def tratto(path, y_from):
        """lunghezza del percorso principale a partire dal punto in cui la linea verticale a +-1,2 mm vale y_from"""
        k = 5  # punto (1,2; yC)
        return abs(y_from - yC) + _len(path[k:])
    via_l = 1.6
    lung = {
        "D- da B7": _len(dn),
        "D+ da B6": _len(dp),
        "D- da A7": _len(a7) + via_l + 1.6 + via_l + tratto(dn, yV2),
        "D+ da A6": _len(a6) + via_l + 1.6 + via_l + tratto(dp, yV1),
        "D- ramo aperto (A7 se la spina usa B7)": _len(a7) + 1.6 + 2 * via_l,
        "D+ ramo aperto (A6 se la spina usa B6)": _len(a6) + 1.6 + 2 * via_l,
        "D- ramo aperto (B7 se la spina usa A7)": _len(dn[:3]) + (yW - yV2),
        "D+ ramo aperto (B6 se la spina usa A6)": _len(dp[:3]) + (yW - yV1),
    }
    zona = (X(-1.7) - OX, X(1.7) - OX, Q + 0.4 - OY, yU + 0.4 - OY)
    return zona, lung
