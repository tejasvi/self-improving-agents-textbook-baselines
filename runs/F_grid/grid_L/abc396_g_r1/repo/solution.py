import sys


def wht(a, W):
    # Walsh-Hadamard transform using the rotating-bit trick (no strided blocks).
    for _ in range(W):
        lo = a[0::2]
        hi = a[1::2]
        a = [x + y for x, y in zip(lo, hi)] + [x - y for x, y in zip(lo, hi)]
    return a


def main():
    data = sys.stdin.read().split()
    H = int(data[0])
    W = int(data[1])
    n = 1 << W
    cnt = [0] * n
    for s in data[2:2 + H]:
        cnt[int(s, 2)] += 1

    g = [0] * n
    for x in range(n):
        p = bin(x).count("1")
        g[x] = min(p, W - p)

    F = wht(cnt, W)
    G = wht(g, W)
    P = [f * h for f, h in zip(F, G)]
    R = wht(P, W)
    best = None
    for v in R:
        v //= n
        if best is None or v < best:
            best = v
    print(best)


if __name__ == "__main__":
    main()
