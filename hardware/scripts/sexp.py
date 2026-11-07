import re
TOK = re.compile(r'\s*(\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+)', re.S)


class Sym(str):
    pass


def _unq(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            n = s[i + 1]
            out.append('\n' if n == 'n' else n)
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def parse(text):
    stack = [[]]
    for m in TOK.finditer(text):
        t = m.group(1)
        if t == '(':
            stack.append([])
        elif t == ')':
            x = stack.pop()
            stack[-1].append(x)
        elif t.startswith('"'):
            stack[-1].append(_unq(t[1:-1]))
        else:
            stack[-1].append(Sym(t))
    return stack[0]


def q(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def dump(x, ind=0):
    if isinstance(x, list):
        if not x:
            return "()"
        if all(not isinstance(e, list) for e in x):
            return "(" + " ".join(dump(e) for e in x) + ")"
        out = "(" + dump(x[0])
        for e in x[1:]:
            if isinstance(e, list):
                out += "\n" + "\t" * (ind + 1) + dump(e, ind + 1)
            else:
                out += " " + dump(e)
        return out + "\n" + "\t" * ind + ")"
    if isinstance(x, Sym):
        return str(x)
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, (int, float)):
        s = f"{x:.4f}".rstrip('0').rstrip('.')
        return '0' if s in ('-0', '') else s
    return q(x)


def find(x, key):
    return [e for e in x if isinstance(e, list) and e and e[0] == key]


def find1(x, key):
    r = find(x, key)
    return r[0] if r else None
