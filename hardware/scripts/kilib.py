"""Loading and flattening of KiCad symbol libraries."""
import copy
from sexp import parse, find, find1, Sym

STD = "C:/Program Files/KiCad/10.0/share/kicad/symbols"


class Library:
    def __init__(self, extra=None):
        self.files = {}
        self.extra = extra or {}

    def _load(self, lib):
        if lib not in self.files:
            path = self.extra.get(lib, f"{STD}/{lib}.kicad_sym")
            root = parse(open(path, encoding="utf-8").read())[0]
            self.files[lib] = {s[1]: s for s in find(root, "symbol")}
        return self.files[lib]

    def flat(self, lib, name):
        syms = self._load(lib)
        s = copy.deepcopy(syms[name])
        ext = find1(s, "extends")
        if not ext:
            return s
        parent = self.flat(lib, ext[1])
        out = [Sym("symbol"), name]
        child_props = {p[1]: p for p in find(s, "property")}
        for e in parent[2:]:
            if isinstance(e, list) and e and e[0] == "property":
                out.append(child_props.pop(e[1], e))
            elif isinstance(e, list) and e and e[0] == "symbol":
                sub = copy.deepcopy(e)
                sub[1] = name + sub[1][len(ext[1]):]
                out.append(sub)
            else:
                out.append(e)
        for p in child_props.values():
            out.append(p)
        # child-level flags (in_bom etc.) override
        for e in s[2:]:
            if isinstance(e, list) and e and e[0] not in ("property", "extends", "symbol"):
                for i, pe in enumerate(out):
                    if isinstance(pe, list) and pe and pe[0] == e[0]:
                        out[i] = e
        return out

    def for_schematic(self, lib_id):
        lib, name = lib_id.split(":")
        s = self.flat(lib, name)
        s[1] = lib_id
        return s


def pins(sym):
    """Return {number: (x, y, rot, name, type)} of all pins in a flattened symbol."""
    res = {}

    def walk(n):
        for e in n:
            if isinstance(e, list) and e and e[0] == "pin":
                at = find1(e, "at")
                res[find1(e, "number")[1]] = (float(at[1]), float(at[2]), int(float(at[3])),
                                              find1(e, "name")[1], str(e[1]))
            elif isinstance(e, list) and e and e[0] == "symbol":
                walk(e)
    walk(sym)
    return res


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    L = Library()
    for lid in sys.argv[1:]:
        s = L.for_schematic(lid)
        print("##", lid, {p[1]: p[2] for p in find(s, "property") if p[1] in ("Reference", "Footprint")})
        for k, v in sorted(pins(s).items(), key=lambda kv: kv[0]):
            print("   ", k, v)
