import sys

def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 1029:
        print("No")
        return
    S2t = V2 + 3 * V3  # P12+P13+P23 must equal this
    def ln(a, b):
        return b - a if b > a else 0
    # per-axis patterns: cube1 at 0, cube2 at p, cube3 at q
    pats = {}
    R = range(-14, 15)
    for p in R:
        for q in R:
            s = (0, p, q)
            key = (ln(max(s[0], s[1]), min(s[0], s[1]) + 7),
                   ln(max(s[0], s[2]), min(s[0], s[2]) + 7),
                   ln(max(s[1], s[2]), min(s[1], s[2]) + 7),
                   ln(max(s), min(s) + 7))
            if key not in pats:
                pats[key] = (p, q)
    keys = list(pats.keys())
    # precompute (y,z) combos
    yz = []
    for j in keys:
        for k in keys:
            yz.append((j[0] * k[0], j[1] * k[1], j[2] * k[2], j[3] * k[3], j, k))
    for x in keys:
        x0, x1, x2, x3 = x
        for a12, a13, a23, a123, j, k in yz:
            if x0 * a12 + x1 * a13 + x2 * a23 == S2t and x3 * a123 == V3:
                xs = pats[x]; ys = pats[j]; zs = pats[k]
                print("Yes")
                print(0, 0, 0, xs[0], ys[0], zs[0], xs[1], ys[1], zs[1])
                return
    print("No")

main()
