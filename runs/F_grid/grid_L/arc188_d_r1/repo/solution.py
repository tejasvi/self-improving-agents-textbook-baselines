import sys
from itertools import permutations

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    B = [int(x) for x in data[1 + n:1 + 2 * n]]

    # Exhaustive search over all triples of coordinate permutations.
    # Exact but only feasible for small N ((N!)^3 candidates).
    perms = list(permutations(range(1, n + 1)))
    found = set()
    for p1 in perms:
        for p2 in perms:
            for p3 in perms:
                vecs = []
                for i in range(n):
                    s = (p1[i], p2[i], p3[i])
                    vecs.append((s, 0, i))
                    vecs.append((s[::-1], 1, i))
                if len(set(v[0] for v in vecs)) != 2 * n:
                    continue
                order = sorted(range(2 * n), key=lambda j: vecs[j][0])
                a = [0] * n
                b = [0] * n
                for rank, j in enumerate(order, 1):
                    _, kind, i = vecs[j]
                    if kind == 0:
                        a[i] = rank
                    else:
                        b[i] = rank
                found.add((tuple(a), tuple(b)))

    cnt = 0
    for a, b in found:
        if list(a) != A:
            continue
        ok = True
        for i in range(n):
            if B[i] != -1 and b[i] != B[i]:
                ok = False
                break
        if ok:
            cnt += 1
    print(cnt % MOD)


if __name__ == "__main__":
    main()
