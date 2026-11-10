"""Colori, luci e render del concept voxel di PoliClock.

La geometria viene tutta da build123d (mechanical/cad/concept_voxel.py, da
lanciare prima): qui si importano le parti STL, si assegnano i colori e si
fanno i render. Il quadrante sul display è solo illustrativo.

Uso (dalla radice del repository):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --background \\
      --python mechanical/blender/render_concept.py
Uscite:
  assets/renders/concept-{fronte,tre-quarti,lato,retro,esploso,sezione}.png
  mechanical/blender/policlock_concept.blend
"""

import json
import math
import os

import bpy

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PARTI = os.path.join(RADICE, "mechanical", "prints", "concept")
OUT = os.path.join(RADICE, "mechanical", "cad", "out", "concept")
RENDERS = os.path.join(RADICE, "assets", "renders")
BLEND = os.path.join(RADICE, "mechanical", "blender", "policlock_concept.blend")

DATI = json.load(open(os.path.join(OUT, "concept.json"), encoding="utf-8"))
Q = DATI["quote"]
Z_MEDIO = (Q["z_cima"]) / 2


def pulisci():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = "METRIC"
    s.unit_settings.scale_length = 0.001
    s.unit_settings.length_unit = "MILLIMETERS"


def lineare(c):
    """sRGB (0-1) -> lineare, per i colori definiti in build123d."""
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


def materiale(nome, colore, rough=0.55, emissione=0.0, metal=0.0, alpha=1.0):
    m = bpy.data.materials.new(nome)
    m.diffuse_color = (*colore, alpha)
    if m.node_tree is None:
        m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
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


def collezione(nome):
    c = bpy.data.collections.new(nome)
    bpy.context.scene.collection.children.link(c)
    return c


def sposta_in(o, coll):
    for c in o.users_collection:
        c.objects.unlink(o)
    coll.objects.link(o)


def importa(percorso, nome, mat, coll):
    bpy.ops.wm.stl_import(filepath=percorso)
    o = bpy.context.selected_objects[0]
    o.name = nome
    o.data.materials.clear()
    o.data.materials.append(mat)
    sposta_in(o, coll)
    return o


def testo(stringa, pos, dim, mat, coll):
    cu = bpy.data.curves.new(stringa, "FONT")
    cu.body = stringa
    cu.size = dim
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    o = bpy.data.objects.new("quadrante " + stringa, cu)
    o.location = pos
    o.rotation_euler = (math.radians(90), 0, 0)
    o.data.materials.append(mat)
    coll.objects.link(o)
    return o


def costruisci():
    rough = {"oro": 0.3, "nero": 0.4, "grigio": 0.35, "base": 0.6, "pelle": 0.6}
    metal = {"oro": 0.7, "grigio": 0.5}
    M = {k: materiale(k, lineare(v), rough.get(k, 0.55), metal=metal.get(k, 0.0)) for k, v in DATI["colori"].items()}
    c_parti = collezione("Parti stampate")
    c_ing = collezione("Ingombri (non stampati)")
    c_disp = collezione("Quadrante")
    oggetti = {}
    for n, info in DATI["parti"].items():
        oggetti[n] = importa(os.path.join(PARTI, n + ".stl"), n, M[info["colore"]], c_parti)

    m_pcb = materiale("PCB", (0.03, 0.30, 0.10), 0.5)
    m_ing = materiale("ingombro", (0.85, 0.45, 0.1), 0.5)
    m_zav = materiale("zavorra", (0.45, 0.45, 0.5), 0.3, metal=0.9)
    m_rtc = materiale("modulo RTC", (0.05, 0.05, 0.12), 0.5)
    m_usb = materiale("spina USB", (0.85, 0.85, 0.85), 0.4)
    for n, fn in DATI["ingombri"].items():
        mat = m_ing
        if "scheda" in n or "modulo display" in n:
            mat = m_pcb
        elif "zavorra" in n:
            mat = m_zav
        elif "DS3231" in n:
            mat = m_rtc
        elif "USB-C (sovrastampo)" in n:
            mat = m_usb
        o = importa(os.path.join(OUT, fn), "ingombro " + n, mat, c_ing)
        if "sovrastampo" in n:      # la spina del cavo si vede anche da fuori
            sposta_in(o, c_parti)
            oggetti["spina_usb"] = o
        if n == "modulo display":
            oggetti["modulo_display"] = o

    # Vetro e quadrante illustrativo davanti al modulo
    yv = Q["faccia_y"] + 3.0 - 0.05
    zd = Q["display_z"]
    bpy.ops.mesh.primitive_cylinder_add(radius=37.5 / 2, depth=0.4, location=(0, yv, zd),
                                        rotation=(math.radians(90), 0, 0), vertices=96)
    vetro = bpy.context.active_object
    vetro.name = "vetro display"
    vetro.data.materials.append(materiale("vetro", (0.004, 0.004, 0.008), 0.08))
    sposta_in(vetro, c_disp)
    m_cifre = materiale("cifre", (0.80, 0.88, 1.0), 0.5, emissione=7.0)
    m_dati = materiale("dati", (0.40, 0.78, 1.0), 0.5, emissione=5.0)
    yt = yv - 0.35
    quadrante = [testo("10:42", (0, yt, zd + 2.0), 11.0, m_cifre, c_disp),
                 testo("lun 10 nov", (0, yt, zd + 11.0), 3.5, m_dati, c_disp),
                 testo("21,5°C  48%", (0, yt, zd - 8.5), 3.5, m_dati, c_disp)]
    oggetti["vetro"] = vetro

    # Cavetto display (solo per la sezione)
    cu = bpy.data.curves.new("cavetto", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 2.2
    sp = cu.splines.new("POLY")
    pts = DATI["percorso_cavo"]
    sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        sp.points[i].co = (p[0], p[1], p[2], 1.0)
    cav = bpy.data.objects.new("cavetto display", cu)
    cav.data.materials.append(materiale("cavetto", (0.75, 0.12, 0.6), 0.5))
    c_ing.objects.link(cav)

    # Cavo USB che scende dal retro
    bpy.ops.mesh.primitive_cylinder_add(radius=1.9, depth=40.0, location=(-18.7, 82.0, 6.0),
                                        rotation=(math.radians(90 - 12), 0, 0), vertices=24)
    cavo = bpy.context.active_object
    cavo.name = "cavo USB"
    cavo.data.materials.append(m_usb)
    sposta_in(cavo, c_parti)
    return oggetti, quadrante


def scena():
    s = bpy.context.scene
    w = bpy.data.worlds.new("mondo")
    s.world = w
    if w.node_tree is None:
        w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.86, 0.87, 0.9, 1.0)
    bg.inputs["Strength"].default_value = 0.55
    for nome, loc, en, dim in (("luce chiave", (-300, -340, 420), 2.0e6, 240),
                               ("luce riempimento", (360, -200, 200), 7e5, 280),
                               ("luce controluce", (80, 420, 360), 1.1e6, 220)):
        ld = bpy.data.lights.new(nome, "AREA")
        ld.energy = en
        ld.size = dim
        lo = bpy.data.objects.new(nome, ld)
        lo.location = loc
        s.collection.objects.link(lo)
        tc = lo.constraints.new("TRACK_TO")
        tc.target = bersaglio(Z_MEDIO)
    bpy.ops.mesh.primitive_plane_add(size=1200, location=(0, 0, -0.05))
    p = bpy.context.active_object
    p.name = "tavolo"
    p.data.materials.append(materiale("tavolo", (0.8, 0.8, 0.82), 0.8))
    s.render.engine = "BLENDER_EEVEE"
    s.eevee.taa_render_samples = 48
    s.render.image_settings.file_format = "PNG"
    s.view_settings.view_transform = "Standard"


_B = {}


def bersaglio(z):
    k = round(z, 1)
    if k not in _B:
        e = bpy.data.objects.new(f"bersaglio {k}", None)
        e.location = (0, 0, z)
        bpy.context.scene.collection.objects.link(e)
        _B[k] = e
    return _B[k]


def camera(nome, pos, z=Z_MEDIO, orto=None, lente=70):
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
    co.constraints.new("TRACK_TO").target = bersaglio(z)
    return co


def visibile(nome_coll, si):
    bpy.data.collections[nome_coll].hide_render = not si


def render(nome, cam, res=(1000, 1250)):
    s = bpy.context.scene
    s.camera = cam
    s.render.resolution_x, s.render.resolution_y = res
    s.render.filepath = os.path.join(RENDERS, nome)
    bpy.ops.render.render(write_still=True)
    print("render:", nome)


def main():
    pulisci()
    oggetti, quadrante = costruisci()
    scena()
    os.makedirs(RENDERS, exist_ok=True)
    h = Q["z_cima"]

    visibile("Ingombri (non stampati)", False)
    render("concept-fronte.png", camera("cam fronte", (0, -700, Z_MEDIO), orto=h * 1.12))
    render("concept-tre-quarti.png", camera("cam tre quarti", (-300, -380, 200), z=Z_MEDIO - 4, lente=70))
    render("concept-lato.png", camera("cam lato", (-700, 0, Z_MEDIO), orto=h * 1.12))
    render("concept-retro.png", camera("cam retro", (60, 700, Z_MEDIO), orto=h * 1.12))

    # Esploso: parti spostate lungo gli offset di build123d, tutto alzato di
    # SOLLEVA perché il fondo della base (spostato in basso) resti sopra il tavolo;
    # il modulo display va a lato della testa
    SOLLEVA = 40.0
    orig = {}
    for o in bpy.data.collections["Parti stampate"].objects:
        orig[o.name] = tuple(o.location)
        dx, dy, dz = DATI["parti"].get(o.name, {"esploso": (0, 0, 0)})["esploso"]
        o.location = (o.location[0] + dx, o.location[1] + dy, o.location[2] + dz + SOLLEVA)
    extra = [oggetti["vetro"], oggetti["modulo_display"], *quadrante]
    spost = (58.0, -10.0, 62.0 + SOLLEVA)
    for o in extra:
        orig[o.name] = tuple(o.location)
        o.location = (o.location[0] + spost[0], o.location[1] + spost[1], o.location[2] + spost[2])
    oggetti["modulo_display"].users_collection[0].objects.unlink(oggetti["modulo_display"])
    bpy.data.collections["Quadrante"].objects.link(oggetti["modulo_display"])
    render("concept-esploso.png", camera("cam esploso", (-380, -470, 260), z=Z_MEDIO + 30, lente=55),
           res=(1100, 1400))
    for o in list(bpy.data.collections["Parti stampate"].objects) + extra:
        o.location = orig[o.name]

    # Sezione sul piano X = 0: si toglie la metà X > 0 e si guarda da +X
    visibile("Ingombri (non stampati)", True)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(150.0, 0, 100.0))
    taglio = bpy.context.active_object
    taglio.name = "taglio sezione"
    taglio.scale = (300.0, 400.0, 400.0)
    taglio.hide_render = True
    taglio.hide_viewport = True
    mods = []
    for o in bpy.data.objects:
        if o.type == "MESH" and o.name not in ("taglio sezione", "tavolo") and not o.name.startswith("ingombro"):
            m = o.modifiers.new("sezione", "BOOLEAN")
            m.operation = "DIFFERENCE"
            m.object = taglio
            mods.append((o, m))
    for o in quadrante:
        o.hide_render = True
    render("concept-sezione.png", camera("cam sezione", (700, 0, Z_MEDIO), orto=h * 1.12))
    for o, m in mods:
        o.modifiers.remove(m)
    for o in quadrante:
        o.hide_render = False
    visibile("Ingombri (non stampati)", False)

    bpy.context.scene.camera = bpy.data.objects["cam tre quarti"]
    bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=True)
    print("salvato:", BLEND)


main()
