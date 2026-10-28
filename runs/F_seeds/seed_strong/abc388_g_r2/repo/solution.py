import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n

    # 1-indexed: nxt[p] = first 1-indexed q with A[q] >= 2*A[p] (n+1 if none)
    c = [0] * (n + 2)
    for p in range(1, n + 1):
        nx = bisect_left(A, 2 * A[p - 1]) + 1
        c[p] = p - nx

    # sparse table over c[1..n]; index 0 and n+1 are dummies
    sp = [c]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        sp.append(list(map(min, prev[:len(prev) - half], prev[half:])))
        k += 1

    out = []
    for _ in range(q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        m = R - L + 1
        lo, hi = 0, m // 2
        while lo < hi:
            K = (lo + hi + 1) >> 1
            # min of c[L..L+K-1]
            length = K
            lg = length.bit_length() - 1
            t = sp[lg]
            mn = t[L]
            v = t[L + K - (1 << lg)]
            if v < mn:
                mn = v
            if mn + m >= K:
                lo = K
            else:
                hi = K - 1
        out.append(lo)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
