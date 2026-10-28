import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubes = []
    idx = 1
    for _ in range(n):
        vals = [int(v) for v in data[idx:idx + 6]]
        idx += 6
        cubes.append((vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]))

    ans = [0] * n
    S = 101
    for a in range(3):
        b_ax = (a + 1) % 3
        c_ax = (a + 2) % 3
        # right[p]: flat grid over (b, c) of ids of cuboids whose max-a face is at p
        right = {}
        lefts = []
        for i in range(n):
            c = cubes[i]
            lo_a, hi_a = c[a], c[a + 3]
            lo_b, hi_b = c[b_ax], c[b_ax + 3]
            lo_c, hi_c = c[c_ax], c[c_ax + 3]
            g = right.get(hi_a)
            if g is None:
                g = [-1] * (S * S)
                right[hi_a] = g
            w = hi_c - lo_c
            fill = [i] * w
            for bb in range(lo_b, hi_b):
                base = bb * S + lo_c
                g[base:base + w] = fill
            lefts.append((lo_a, lo_b, hi_b, lo_c, hi_c))
        for j in range(n):
            lo_a, lo_b, hi_b, lo_c, hi_c = lefts[j]
            g = right.get(lo_a)
            if g is None:
                continue
            owners = set()
            for bb in range(lo_b, hi_b):
                base = bb * S
                owners.update(g[base + lo_c: base + hi_c])
            owners.discard(-1)
            if owners:
                ans[j] += len(owners)
                for i in owners:
                    ans[i] += 1
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
