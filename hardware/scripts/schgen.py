"""Tiny KiCad 10 schematic writer: symbols on a grid, connections via stubs + labels/power symbols."""
import math
import uuid as _uuid
from sexp import dump, find, find1, Sym
from kilib import pins

S = Sym
G = 1.27


def U(seed):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "policlock/" + seed))


def snap(v):
    return round(round(v / G) * G, 4)


def font(size=1.27, hide=False, justify=None, bold=False):
    f = [S("font"), [S("size"), size, size]]
    if bold:
        f.append([S("bold"), S("yes")])
    e = [S("effects"), f]
    if justify:
        e.append([S("justify")] + [S(j) for j in justify.split()])
    if hide:
        e.append([S("hide"), S("yes")])
    return e


PWRN = {}
POWER_UP = {"+3V3", "+5V", "VBUS"}


class Comp:
    def __init__(self, sheet, lib_id, sym, ref, x, y, rot):
        self.sheet, self.lib_id, self.sym, self.ref = sheet, lib_id, sym, ref
        self.x, self.y, self.rot = x, y, rot
        self.pins = pins(sym)

    def _xf(self, px, py):
        # lib coords (y up) -> rotated -> schematic (y down)
        a = math.radians(self.rot)
        rx = px * math.cos(a) - py * math.sin(a)
        ry = px * math.sin(a) + py * math.cos(a)
        return snap(self.x + rx), snap(self.y - ry)

    def pin_end(self, num):
        px, py, prot, *_ = self.pins[num]
        return self._xf(px, py)

    def pin_out(self, num):
        """Unit vector (schematic coords) pointing away from the body."""
        prot = (self.pins[num][2] + self.rot) % 360
        out = (prot + 180) % 360
        return {0: (1, 0), 90: (0, -1), 180: (-1, 0), 270: (0, 1)}[out]


class Sheet:
    def __init__(self, project, name, filename, root_uuid, path, paper="A3", title="", comment=""):
        self.project, self.name, self.filename = project, name, filename
        self.uuid = U(project + "/" + filename)
        self.root_uuid = root_uuid
        self.path = path  # instance path for symbols in this sheet
        self.paper, self.title, self.comment = paper, title, comment
        self.items = []
        self.libsyms = {}
        self.comps = []
        self.n = 0
        self.sheets = []

    def uid(self, tag):
        self.n += 1
        return U(f"{self.project}/{self.filename}/{tag}/{self.n}")

    # ---------------------------------------------------------- symbols
    def add(self, lib, lib_id, ref, value, x, y, rot=0, fp="", ds="", lcsc="", dnp=False,
            in_bom=True, desc="", extra=None, ref_off=None, val_off=None, hide_val=False):
        sym = lib.for_schematic(lib_id)
        self.libsyms[lib_id] = sym
        x, y = snap(x), snap(y)
        c = Comp(self, lib_id, sym, ref, x, y, rot)
        props = {p[1]: p for p in find(sym, "property")}
        is_power = ref.startswith("#")

        def ppos(key, default):
            p = props.get(key)
            if p is not None:
                at = find1(p, "at")
                px, py = c._xf(float(at[1]), float(at[2]))
                return px, py, float(at[3]) if len(at) > 3 else 0
            return x + default[0], y + default[1], 0

        fields = []

        def field(key, val, hide, off=None, just=None):
            if off is not None:
                px, py, pr = x + off[0], y + off[1], 0
            else:
                px, py, pr = ppos(key, (0, 0))
                if rot in (90, 270) and pr in (0, 90):
                    pr = 90 - pr
            if pr == 90 and rot == 0:
                pr = 90
            f = [S("property"), key, val, [S("at"), px, py, pr], font(hide=hide, justify=just)]
            fields.append(f)

        if ref_off is None and not is_power and lib_id.startswith("Device:"):
            ref_off, val_off = (2.54, -1.27), (2.54, 1.27)
        field("Reference", ref, is_power, ref_off, "left" if ref_off else None)
        field("Value", value, hide_val, val_off, "left" if val_off else None)
        field("Footprint", fp or props.get("Footprint", [0, 0, ""])[2], True)
        field("Datasheet", ds or props.get("Datasheet", [0, 0, ""])[2], True)
        field("Description", desc or props.get("Description", [0, 0, ""])[2], True)
        if not is_power:
            field("LCSC", lcsc, True)
        for k, v in (extra or {}).items():
            field(k, v, True)
        node = [S("symbol"), [S("lib_id"), lib_id], [S("at"), x, y, rot], [S("unit"), 1],
                [S("exclude_from_sim"), S("no")], [S("in_bom"), S("yes" if in_bom else "no")],
                [S("on_board"), S("yes")], [S("dnp"), S("yes" if dnp else "no")],
                [S("uuid"), self.uid("sym" + ref)]] + fields
        for num in c.pins:
            node.append([S("pin"), num, [S("uuid"), self.uid("pin")]])
        node.append([S("instances"), [S("project"), self.project,
                                      [S("path"), self.path, [S("reference"), ref], [S("unit"), 1]]]])
        self.items.append(node)
        self.comps.append(c)
        return c

    # ---------------------------------------------------------- connections
    def wire(self, a, b):
        self.items.append([S("wire"), [S("pts"), [S("xy"), a[0], a[1]], [S("xy"), b[0], b[1]]],
                           [S("stroke"), [S("width"), 0], [S("type"), S("default")]],
                           [S("uuid"), self.uid("w")]])

    def stub(self, c, num, length=2.54):
        x0, y0 = c.pin_end(num)
        dx, dy = c.pin_out(num)
        x1, y1 = snap(x0 + dx * length), snap(y0 + dy * length)
        self.wire((x0, y0), (x1, y1))
        return (x1, y1), (dx, dy)

    def label(self, pos, d, net, kind="label"):
        ang = {(1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270}[d]
        if kind == "label":
            just = "left bottom" if ang in (0, 90) else "right bottom"
            self.items.append([S("label"), net, [S("at"), pos[0], pos[1], ang],
                               font(justify=just), [S("uuid"), self.uid("l")]])
        else:
            just = "left" if ang in (0, 90) else "right"
            self.items.append([S("global_label"), net, [S("shape"), S("bidirectional")],
                               [S("at"), pos[0], pos[1], ang], [S("fields_autoplaced"), S("yes")],
                               font(justify=just), [S("uuid"), self.uid("g")],
                               [S("property"), "Intersheetrefs", "${INTERSHEET_REFS}",
                                [S("at"), pos[0], pos[1], 0], font(hide=True)]])

    def power(self, lib, net, pos, d):
        lib_id = "power:" + net
        natural = (0, -1) if net in POWER_UP or net.startswith("+") else (0, 1)
        if net == "PWR_FLAG":
            natural = (0, -1)

        def ang(v):
            return math.degrees(math.atan2(-v[1], v[0])) % 360
        rot = int(round((ang(d) - ang(natural)) % 360))
        PWRN[self.project] = PWRN.get(self.project, 0) + 1
        ref = f"#PWR{PWRN[self.project]:03d}"
        c = self.add(lib, lib_id, ref, net, pos[0], pos[1], rot=rot)
        return c

    def conn(self, lib, c, num, net, kind=None, length=None):
        """Connect pin to net. Power nets (GND,+3V3,+5V,VBUS) get power symbols."""
        if length is None:
            small = c.lib_id.startswith(("Device:", "Connector:TestPoint"))
            length = 2.54 if small else 7.62
        pos, d = self.stub(c, num, length)
        if kind is None:
            kind = "power" if net in ("GND", "+3V3", "+5V", "VBUS") else "label"
        if kind == "power":
            self.power(lib, net, pos, d)
        else:
            self.label(pos, d, net, kind)

    def nc(self, c, num):
        x, y = c.pin_end(num)
        self.items.append([S("no_connect"), [S("at"), x, y], [S("uuid"), self.uid("nc")]])

    def flag(self, lib, net, x, y):
        """PWR_FLAG + power symbol of net, joined by a short wire."""
        x, y = snap(x), snap(y)
        PWRN[self.project] = PWRN.get(self.project, 0) + 1
        self.add(lib, "power:PWR_FLAG", f"#FLG{PWRN[self.project]:03d}", "PWR_FLAG", x, y)
        self.wire((x, y), (x, y + 2.54))
        d = (0, 1)
        self.power(lib, net, (x, snap(y + 2.54)), d)

    def text(self, s, x, y, size=1.27, bold=False):
        self.items.append([S("text"), s, [S("exclude_from_sim"), S("no")], [S("at"), snap(x), snap(y), 0],
                           font(size=size, justify="left top", bold=bold), [S("uuid"), self.uid("t")]])

    def box(self, x1, y1, x2, y2, title=None):
        self.items.append([S("rectangle"), [S("start"), x1, y1], [S("end"), x2, y2],
                           [S("stroke"), [S("width"), 0], [S("type"), S("dash")]],
                           [S("fill"), [S("type"), S("none")]], [S("uuid"), self.uid("r")]])
        if title:
            self.text(title, x1 + 1.27, y1 + 1.27, 2.0, True)

    def subsheet(self, name, filename, x, y, w, h, page):
        sid = U(self.project + "/" + filename)
        node = [S("sheet"), [S("at"), x, y], [S("size"), w, h], [S("exclude_from_sim"), S("no")],
                [S("in_bom"), S("yes")], [S("on_board"), S("yes")], [S("dnp"), S("no")],
                [S("fields_autoplaced"), S("yes")],
                [S("stroke"), [S("width"), 0.1524], [S("type"), S("solid")]],
                [S("fill"), [S("color"), 0, 0, 0, 0.0]], [S("uuid"), sid],
                [S("property"), "Sheetname", name, [S("at"), x, y - 0.7116, 0], font(justify="left bottom")],
                [S("property"), "Sheetfile", filename, [S("at"), x, y + h + 0.5846, 0],
                 font(justify="left top")],
                [S("instances"), [S("project"), self.project,
                                  [S("path"), "/" + self.root_uuid, [S("page"), str(page)]]]]]
        self.items.append(node)
        return sid

    # ---------------------------------------------------------- output
    def write(self, path, is_root):
        tb = [S("title_block"), [S("title"), self.title or self.name], [S("date"), "2026-11-07"],
              [S("rev"), "0.1"], [S("company"), "PoliClock"]]
        if self.comment:
            for i, line in enumerate(self.comment.split("\n")[:4], 1):
                tb.append([S("comment"), i, line])
        doc = [S("kicad_sch"), [S("version"), 20250610], [S("generator"), "eeschema"],
               [S("generator_version"), "10.0"], [S("uuid"), self.uuid if not is_root else self.root_uuid],
               [S("paper"), self.paper], tb,
               [S("lib_symbols")] + list(self.libsyms.values())] + self.items
        if is_root:
            doc.append([S("sheet_instances"), [S("path"), "/", [S("page"), "1"]]])
        doc.append([S("embedded_fonts"), S("no")])
        open(path, "w", encoding="utf-8", newline="\n").write(dump(doc) + "\n")
