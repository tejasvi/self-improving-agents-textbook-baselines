import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = 101
    S2 = S * S
    cubes = []
    idx = 1
    for _ in range(n):
        vals = [int(x) for x in data[idx:idx + 6]]
        idx += 6
        cubes.append(vals)

    pairs = set()
    for a in range(3):
        u_ax, v_ax = [k for k in range(3) if k != a]
        plus = [-1] * (S * S2)   # owner whose max face is on plane c
        minus = [-1] * (S * S2)  # owner whose min face is on plane c
        for i, p in enumerate(cubes):
            a1, a2 = p[a], p[a + 3]
            u1, u2 = p[u_ax], p[u_ax + 3]
            v1, v2 = p[v_ax], p[v_ax + 3]
            L = v2 - v1
            block = [i] * L
            for u in range(u1, u2):
                base = u * S + v1
                b2 = a2 * S2 + base
                plus[b2:b2 + L] = block
                b1 = a1 * S2 + base
                minus[b1:b1 + L] = block
        # any unit square with plus owner i and minus owner j => share face
        for k in range(S * S2):
            pi = plus[k]
            if pi < 0:
                continue
            mj = minus[k]
            if mj < 0 or mj == pi:
                continue
            if pi < mj:
                pairs.add((pi, mj))
            else:
                pairs.add((mj, pi))

    cnt = [0] * n
    for i, j in pairs:
        cnt[i] += 1
        cnt[j] += 1
    sys.stdout.write("\n".join(map(str, cnt)) + "\n")


main()
