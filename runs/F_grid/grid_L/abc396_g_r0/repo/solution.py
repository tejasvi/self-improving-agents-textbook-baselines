import sys


def wht(a):
    # In-place unnormalized Walsh-Hadamard transform on a Python list (len = power of 2).
    n = len(a)
    h = 1
    while h < n:
        step = 2 * h
        if h <= n // step:
            # few short-stride passes: slice over offsets j
            for j in range(h):
                lo = a[j:n:step]
                hi = a[j + h:n:step]
                a[j:n:step] = [x + y for x, y in zip(lo, hi)]
                a[j + h:n:step] = [x - y for x, y in zip(lo, hi)]
        else:
            # many blocks: process each block
            for k in range(0, n, step):
                lo = a[k:k + h]
                hi = a[k + h:k + step]
                a[k:k + h] = [x + y for x, y in zip(lo, hi)]
                a[k + h:k + step] = [x - y for x, y in zip(lo, hi)]
        h = step
    return a


def main():
    data = sys.stdin.read().split()
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    N = 1 << W
    cnt = [0] * N
    for s in rows:
        cnt[int(s, 2)] += 1

    g = [0] * N
    for u in range(N):
        p = bin(u).count("1")
        g[u] = min(p, W - p)

    # f(c) = sum_v cnt[v] * g[v ^ c]  via XOR convolution
    Fc = wht(cnt)
    Fg = wht(g)
    prod = [x * y for x, y in zip(Fc, Fg)]
    f = wht(prod)
    best = min(f) // N
    print(best)


if __name__ == "__main__":
    main()
