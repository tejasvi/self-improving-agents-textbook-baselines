import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    xs = [int(v) for v in data[2:2 + m]]
    diff = [0] * (n + 2)

    def add(l, r, v):
        # add v to bridges l..r inclusive (1-indexed), if l <= r
        if l <= r:
            diff[l] += v
            diff[r + 1] -= v

    base = 0
    for k in range(m - 1):
        a, b = xs[k], xs[k + 1]
        if a > b:
            a, b = b, a
        L = b - a
        R = n - L
        if L == R:
            base += L
            continue
        if L < R:
            base += L
            # shorter arc: bridges a..b-1
            add(a, b - 1, R - L)
        else:
            base += R
            # shorter arc: bridges b..n and 1..a-1
            add(b, n, L - R)
            add(1, a - 1, L - R)

    best = None
    cur = 0
    for e in range(1, n + 1):
        cur += diff[e]
        if best is None or cur < best:
            best = cur
    print(base + best)


main()
