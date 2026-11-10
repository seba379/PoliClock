"""Blockout a volumi semplici della poliziotta chibi (PoliClock, fase 1).

Volumi indicativi per proporzioni e ingombri, NON la scultura finale: la
forma artistica si modella a mano in Blender partendo da questo file.
La base è importata dallo studio build123d (mechanical/cad/studio_base.py),
quindi lanciare prima quello.

Uso (dalla radice del repository):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background \\
      --python mechanical/blender/blockout_chibi.py
Uscite:
  mechanical/blender/policlock_blockout.blend
  assets/renders/blockout-*.png

Riferimento come in build123d: X destra (guardando da davanti), Y verso il
retro, Z alto, 1 unità = 1 mm, tavolo a Z = 0, asse del corpo in X = 0, Y = 0.
Stile: poliziotta chibi originale, uniforme blu e cappello (DEC-010), nessuna
insegna ufficiale. In piedi sulla base (scelta del proprietario, 2026-11-09).
"""

import math
import os

import bpy
from mathutils import Vector

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PRINTS = os.path.join(RADICE, "mechanical", "prints")
OUT_CAD = os.path.join(RADICE, "mechanical", "cad", "out")
RENDERS = os.path.join(RADICE, "assets", "renders")
BLEND = os.path.join(RADICE, "mechanical", "blender", "policlock_blockout.blend")

# ---------------------------------------------------------------------------
# Quote principali del blockout (mm). Le quote della base vengono dallo
# studio build123d: altezza 24,1, canale del cavo 21 x 6 in X 0, Y 0.
# ---------------------------------------------------------------------------
Z_BASE = 24.1
STIVALI = (Z_BASE, 34.0)
GAMBE = (33.0, 50.0)
GIACCA = (46.0, 80.0)        # busto con giacca svasata in basso
TESTA_C = (0.0, -1.0, 100.0)  # centro della testa
TESTA_DIM = (68.0, 56.0, 70.0)   # il volto deve contenere il modulo display con l'aletta
DISPLAY_C = (0.0, -28.8, 103.0)  # centro del vetro, faccia anteriore
DISPLAY_TONDO_D = 37.5        # segnaposto OPEN-016
DISPLAY_ATTIVO_D = 32.4
DISPLAY_PCB = (38.0, 45.5, 4.8)  # segnaposto, aletta dei pin verso il basso
CAPPELLO = (128.0, 148.0)
CANALE = (21.0, 6.0)


# ---------------------------------------------------------------------------
# Utilità
# ---------------------------------------------------------------------------
def pulisci():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = "METRIC"
    s.unit_settings.scale_length = 0.001
    s.unit_settings.length_unit = "MILLIMETERS"


def collezione(nome):
    c = bpy.data.collections.new(nome)
    bpy.context.scene.collection.children.link(c)
    return c


def materiale(nome, colore, rough=0.55, emissione=0.0, alpha=1.0, metal=0.0):
    m = bpy.data.materials.new(nome)
    m.diffuse_color = (*colore, alpha)
    nt = m.node_tree if m.node_tree else None
    if nt is None:
        m.use_nodes = True
        nt = m.node_tree
    b = nt.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*colore, 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emissione:
        b.inputs["Emission Color"].default_value = (*colore, 1.0)
        b.inputs["Emission Strength"].default_value = emissione
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except AttributeError:
            pass
    return m


def metti(obj, nome, mat, coll, liscio=True):
    obj.name = nome
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    coll.objects.link(obj)
    if liscio and hasattr(obj.data, "polygons"):
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj


def applica_scala(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def ellissoide(nome, c, dim, mat, coll, seg=64):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=c, segments=seg, ring_count=seg // 2)
    o = bpy.context.active_object
    o.scale = dim
    applica_scala(o)
    return metti(o, nome, mat, coll)


def scatola_tonda(nome, c, dim, raggio, mat, coll, seg=8):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=c)
    o = bpy.context.active_object
    o.scale = dim
    applica_scala(o)
    m = o.modifiers.new("smusso", "BEVEL")
    m.width = raggio
    m.segments = seg
    m.limit_method = "NONE"
    return metti(o, nome, mat, coll)


def cilindro(nome, c, r, h, mat, coll, r2=None, rot=(0, 0, 0), scala=(1, 1, 1), seg=64):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=c, rotation=rot, vertices=seg)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=h, location=c, rotation=rot, vertices=seg)
    o = bpy.context.active_object
    o.scale = scala
    applica_scala(o)
    return metti(o, nome, mat, coll, liscio=False)


def differenza(obj, taglio):
    m = obj.modifiers.new("taglio_" + taglio.name, "BOOLEAN")
    m.operation = "DIFFERENCE"
    m.object = taglio
    taglio.hide_render = True
    taglio.hide_viewport = True


def importa_stl(percorso, nome, mat, coll):
    bpy.ops.wm.stl_import(filepath=percorso)
    o = bpy.context.selected_objects[0]
    return metti(o, nome, mat, coll, liscio=False)


def testo(stringa, pos, dim, mat, coll):
    cu = bpy.data.curves.new(stringa, "FONT")
    cu.body = stringa
    cu.size = dim
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    o = bpy.data.objects.new("testo " + stringa, cu)
    o.location = pos
    o.rotation_euler = (math.radians(90), 0, 0)
    o.data.materials.append(mat)
    coll.objects.link(o)
    return o


# ---------------------------------------------------------------------------
# Modello
# ---------------------------------------------------------------------------
def costruisci():
    M = {
        "base": materiale("base blu notte", (0.035, 0.06, 0.16), 0.5),
        "fondo": materiale("fondo grigio", (0.25, 0.25, 0.27), 0.7),
        "divisa": materiale("divisa blu", (0.06, 0.12, 0.38), 0.6),
        "scuro": materiale("blu scuro cappello", (0.025, 0.04, 0.12), 0.45),
        "nero": materiale("nero stivali", (0.02, 0.02, 0.025), 0.35),
        "pelle": materiale("pelle", (0.85, 0.62, 0.5), 0.6),
        "capelli": materiale("capelli castani", (0.18, 0.09, 0.04), 0.5),
        "oro": materiale("dettagli oro", (0.8, 0.6, 0.18), 0.3, metal=0.8),
        "vetro": materiale("vetro display", (0.005, 0.005, 0.01), 0.08),
        "cornice": materiale("cornice display", (0.02, 0.03, 0.08), 0.35),
        "cifre": materiale("cifre display", (0.75, 0.85, 1.0), 0.5, emissione=6.0),
        "cifre2": materiale("dati display", (0.35, 0.75, 1.0), 0.5, emissione=4.0),
        "pcb": materiale("ingombro PCB", (0.05, 0.35, 0.12), 0.5),
        "ingombro": materiale("ingombro componenti", (0.85, 0.45, 0.1), 0.5),
        "zavorra": materiale("zavorra", (0.45, 0.45, 0.5), 0.3, metal=0.9),
        "cavo": materiale("cavo USB", (0.85, 0.85, 0.85), 0.4),
        "canale": materiale("canale cavo (trasparente)", (0.9, 0.1, 0.1), 0.4, alpha=0.35),
        "rtc": materiale("modulo RTC", (0.05, 0.05, 0.12), 0.5),
        "sht": materiale("modulo SHT40", (0.02, 0.02, 0.02), 0.5),
    }
    c_base = collezione("Base (build123d)")
    c_chibi = collezione("Chibi blockout")
    c_disp = collezione("Display")
    c_ing = collezione("Ingombri interni")
    c_aiuti = collezione("Aiuti (non stampati)")

    # --- Base dallo studio build123d -------------------------------------
    importa_stl(os.path.join(PRINTS, "base-guscio.stl"), "base guscio", M["base"], c_base)
    importa_stl(os.path.join(PRINTS, "base-fondo.stl"), "base fondo (sportello)", M["fondo"], c_base)

    # --- Stivali, gambe, giacca, braccia -----------------------------------
    for s, x in (("sx", -8.0), ("dx", 8.0)):
        scatola_tonda(f"stivale {s}", (x, -6.0, (STIVALI[0] + STIVALI[1]) / 2 + 0.5),
                      (15.0, 25.0, STIVALI[1] - STIVALI[0] + 1.0), 5.0, M["nero"], c_chibi)
        cilindro(f"gamba {s}", (x * 0.9, -1.0, (GAMBE[0] + GAMBE[1]) / 2), 7.6, GAMBE[1] - GAMBE[0],
                 M["divisa"], c_chibi, r2=7.0)
    # giacca: busto arrotondato + svasatura in basso
    scatola_tonda("busto", (0.0, 0.0, 66.0), (34.0, 25.0, 28.0), 10.0, M["divisa"], c_chibi)
    cilindro("falda giacca", (0.0, 0.0, 52.5), 19.5, 13.0, M["divisa"], c_chibi, r2=15.5,
             scala=(1.0, 0.78, 1.0))
    cilindro("cintura", (0.0, 0.0, 58.5), 16.6, 3.0, M["nero"], c_chibi, scala=(1.0, 0.8, 1.0))
    for s, sx in (("sx", -1), ("dx", 1)):
        b = cilindro(f"braccio {s}", (sx * 20.5, 0.0, 66.0), 5.6, 24.0, M["divisa"], c_chibi,
                     r2=6.5, rot=(0, math.radians(-sx * 12), 0))
        ellissoide(f"mano {s}", (sx * 23.0, -0.5, 52.5), (10.0, 10.0, 10.0), M["pelle"], c_chibi, seg=32)
    # spalline e taschino generici (nessuna insegna)
    ellissoide("collo", (0.0, 0.0, 80.0), (16.0, 14.0, 10.0), M["pelle"], c_chibi, seg=32)
    scatola_tonda("colletto", (0.0, -3.0, 79.0), (24.0, 14.0, 5.0), 2.0, M["scuro"], c_chibi, seg=3)
    ellissoide("bottone", (0.0, -12.6, 70.0), (2.6, 1.4, 2.6), M["oro"], c_chibi, seg=16)
    ellissoide("bottone 2", (0.0, -12.6, 63.0), (2.6, 1.4, 2.6), M["oro"], c_chibi, seg=16)

    # --- Testa: forma "squircle" con il volto piatto per il display --------
    scatola_tonda("testa", TESTA_C, TESTA_DIM, 11.0, M["pelle"], c_chibi, seg=10)
    # capelli: calotta più grande della testa, tagliata con un piano davanti
    capelli = scatola_tonda("capelli", (0.0, 1.8, 102.5), (72.0, 58.0, 68.0), 13.0, M["capelli"], c_chibi, seg=10)
    t = scatola_tonda("taglio volto", (0.0, -42.0, 96.0), (120.0, 60.0, 80.0), 0.5, M["capelli"], c_aiuti, seg=1)
    differenza(capelli, t)
    ellissoide("frangia", (0.0, -22.5, 127.0), (64.0, 16.0, 16.0), M["capelli"], c_chibi)
    for s_, sx in (("sx", -1), ("dx", 1)):
        ellissoide(f"ciocca {s_}", (sx * 30.5, -17.0, 98.0), (12.0, 18.0, 50.0), M["capelli"], c_chibi, seg=32)
    ellissoide("chignon", (0.0, 31.0, 102.0), (22.0, 16.0, 20.0), M["capelli"], c_chibi, seg=32)

    # --- Cappello con visiera (generico, senza fregi ufficiali) ----------
    cilindro("fascia cappello", (0.0, 1.0, 132.5), 31.0, 7.0, M["nero"], c_chibi, scala=(1.0, 0.92, 1.0))
    cilindro("calotta cappello", (0.0, 1.5, 141.0), 31.5, 11.0, M["scuro"], c_chibi, r2=36.5,
             scala=(1.0, 0.92, 1.0))
    ellissoide("cupola cappello", (0.0, 1.5, 146.5), (73.0, 67.0, 7.0), M["scuro"], c_chibi)
    cilindro("visiera", (0.0, -26.0, 129.5), 24.0, 2.0, M["nero"], c_chibi,
             rot=(math.radians(16), 0, 0), scala=(1.0, 0.5, 1.0))
    ellissoide("fregio generico", (0.0, -28.4, 134.0), (8.0, 2.0, 7.0), M["oro"], c_chibi, seg=24)

    # --- Display (segnaposto OPEN-016) ------------------------------------
    x, y, z = DISPLAY_C
    bpy.ops.mesh.primitive_torus_add(location=(x, y - 0.2, z), rotation=(math.radians(90), 0, 0),
                                     major_radius=DISPLAY_TONDO_D / 2 + 1.4, minor_radius=1.8,
                                     major_segments=96, minor_segments=16)
    metti(bpy.context.active_object, "cornice display", M["cornice"], c_disp)
    cilindro("vetro display", (x, y + 0.2, z), DISPLAY_TONDO_D / 2, 1.0, M["vetro"], c_disp,
             rot=(math.radians(90), 0, 0))
    yt = y - 0.45
    testo("10:42", (x, yt, z + 2.5), 11.0, M["cifre"], c_disp)
    testo("lun 9 nov", (x, yt, z + 11.5), 3.6, M["cifre2"], c_disp)
    testo("21,5°C  48%", (x, yt, z - 8.0), 3.6, M["cifre2"], c_disp)
    pw, ph, pt = DISPLAY_PCB
    scatola_tonda("modulo display (ingombro)", (x, y + 1.0 + pt / 2, z - (ph - DISPLAY_TONDO_D) / 2),
                  (pw, pt, ph), 0.5, M["pcb"], c_disp, seg=1)
    # spina Dupont sul modulo (pin verso il retro, aletta in basso)
    zs = z - (ph - DISPLAY_TONDO_D) / 2 - ph / 2 + 2.5   # fila dei pin vicino al bordo dell'aletta
    scatola_tonda("spina Dupont lato display", (x, y + 1.0 + pt + 8.25, zs), (17.8, 16.5, 2.54), 0.3,
                  M["ingombro"], c_disp, seg=1)

    # --- Ingombri interni della base (da build123d) -----------------------
    if os.path.isdir(OUT_CAD):
        for f in sorted(os.listdir(OUT_CAD)):
            if not f.endswith(".stl"):
                continue
            n = f[len("ingombro_"):-4].replace("_", " ")
            mat = M["ingombro"]
            if n == "scheda":
                mat = M["pcb"]
            elif n == "zavorra":
                mat = M["zavorra"]
            elif n.startswith("DS3231"):
                mat = M["rtc"]
            elif n.startswith("SHT40 modulo"):
                mat = M["sht"]
            elif "sovrastampo" in n:
                mat = M["cavo"]
            o = importa_stl(os.path.join(OUT_CAD, f), "ingombro " + n, mat, c_ing)
            if "sovrastampo" in n:   # la spina del cavo si vede da fuori
                for cc in o.users_collection:
                    cc.objects.unlink(o)
                c_chibi.objects.link(o)

    # Cavo USB che scende dal retro verso il piano
    cilindro("cavo USB-C", (-16.16, 75.0, 6.0), 1.9, 31.0, M["cavo"], c_chibi,
             rot=(math.radians(90 - 14), 0, 0), seg=24)

    # Canale del cavetto display (trasparente, solo come aiuto)
    zc0, zc1 = Z_BASE - 2.5, 86.0
    scatola_tonda("canale cavetto display", (0.0, 0.0, (zc0 + zc1) / 2), (CANALE[0], CANALE[1], zc1 - zc0),
                  2.0, M["canale"], c_aiuti, seg=2)
    return M


# ---------------------------------------------------------------------------
# Luci, camere, render
# ---------------------------------------------------------------------------
def scena():
    s = bpy.context.scene
    w = bpy.data.worlds.new("mondo")
    s.world = w
    w.color = (0.82, 0.84, 0.88)
    if w.node_tree is None:
        w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.82, 0.84, 0.88, 1.0)
        bg.inputs["Strength"].default_value = 0.65
    for nome, loc, en, dim in (("luce chiave", (-260, -300, 360), 1.6e6, 220),
                               ("luce riempimento", (320, -160, 160), 6e5, 260),
                               ("luce controluce", (60, 360, 300), 9e5, 200)):
        ld = bpy.data.lights.new(nome, "AREA")
        ld.energy = en
        ld.size = dim
        lo = bpy.data.objects.new(nome, ld)
        lo.location = loc
        s.collection.objects.link(lo)
        tc = lo.constraints.new("TRACK_TO")
        tc.target = bersaglio()
    # piano d'appoggio
    bpy.ops.mesh.primitive_plane_add(size=900, location=(0, 0, -0.05))
    p = bpy.context.active_object
    p.name = "tavolo"
    p.data.materials.append(materiale("tavolo", (0.78, 0.78, 0.8), 0.8))
    p.is_shadow_catcher = False


_BERSAGLIO = {}


def bersaglio(z=74.0):
    if z not in _BERSAGLIO:
        e = bpy.data.objects.new(f"bersaglio {z}", None)
        e.location = (0, 0, z)
        bpy.context.scene.collection.objects.link(e)
        _BERSAGLIO[z] = e
    return _BERSAGLIO[z]


def camera(nome, pos, z_bers=74.0, orto=None, lente=70):
    cd = bpy.data.cameras.new(nome)
    if orto:
        cd.type = "ORTHO"
        cd.ortho_scale = orto
    else:
        cd.lens = lente
    cd.clip_end = 5000
    co = bpy.data.objects.new(nome, cd)
    co.location = pos
    bpy.context.scene.collection.objects.link(co)
    tc = co.constraints.new("TRACK_TO")
    tc.target = bersaglio(z_bers)
    return co


def mostra(coll_nome, visibile):
    c = bpy.data.collections.get(coll_nome)
    if c:
        c.hide_render = not visibile


def render(nome, cam, res=(1000, 1200)):
    s = bpy.context.scene
    s.camera = cam
    s.render.resolution_x, s.render.resolution_y = res
    s.render.filepath = os.path.join(RENDERS, nome)
    bpy.ops.render.render(write_still=True)
    print("render:", s.render.filepath)


def motore():
    s = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            s.render.engine = eng
            break
        except TypeError:
            continue
    if s.render.engine.startswith("BLENDER_EEVEE"):
        s.eevee.taa_render_samples = 48
    s.render.image_settings.file_format = "PNG"
    s.render.film_transparent = False
    s.view_settings.view_transform = "AgX"
    print("motore di render:", s.render.engine)


def sezione_base():
    """Guscio tagliato a Z 15 per vedere scheda, moduli e zavorra dall'alto."""
    g = bpy.data.objects["base guscio"]
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 15.0 + 50.0))
    t = bpy.context.active_object
    t.scale = (300, 300, 100)
    t.name = "taglio sezione"
    m = g.modifiers.new("sezione", "BOOLEAN")
    m.operation = "DIFFERENCE"
    m.object = t
    t.hide_render = True
    t.hide_viewport = True
    return m


def main():
    pulisci()
    costruisci()
    scena()
    motore()
    os.makedirs(RENDERS, exist_ok=True)

    mostra("Ingombri interni", False)
    mostra("Aiuti (non stampati)", False)
    render("blockout-fronte.png", camera("cam fronte", (0, -600, 74), orto=172))
    render("blockout-lato.png", camera("cam lato", (600, 0, 74), orto=172))
    render("blockout-retro.png", camera("cam retro", (0, 600, 74), orto=172))
    render("blockout-tre-quarti.png", camera("cam tre quarti", (-260, -330, 170), z_bers=72, lente=75))

    # Sezione della base: chibi nascosta, guscio tagliato, ingombri visibili
    mostra("Chibi blockout", False)
    mostra("Display", False)
    mostra("Ingombri interni", True)
    mod = sezione_base()
    cam = camera("cam sezione base", (0.0, 2.0, 400.0), z_bers=0.0, orto=100)
    cam.constraints.clear()
    cam.rotation_euler = (0, 0, 0)
    render("blockout-sezione-base.png", cam, res=(1100, 1100))
    cam2 = camera("cam sezione base 3/4", (-120, -150, 150), z_bers=8.0, lente=60)
    render("blockout-sezione-base-3q.png", cam2, res=(1200, 1000))
    # ripristina la scena per il file .blend
    bpy.data.objects["base guscio"].modifiers.remove(mod)
    mostra("Chibi blockout", True)
    mostra("Display", True)
    mostra("Ingombri interni", False)

    bpy.context.scene.camera = bpy.data.objects["cam tre quarti"]
    bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=True)
    print("salvato:", BLEND)


main()
