import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    q = int(data[1 + n])
    vals = list(map(int, data[2 + n:2 + n + 2 * q]))

    INF = 10 ** 9
    # g[x]: first index y with A[y] >= 2*A[x]; h[x] = x - g[x]
    h = [0] * n
    for x in range(n):
        g = bisect_left(A, 2 * A[x])
        if g >= n:
            g = INF
        h[x] = x - g

    # sparse table for range minimum
    table = [h]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        span = 1 << (k - 1)
        table.append(list(map(min, prev[:len(prev) - span], prev[span:])))
        k += 1

    out = []
    for i in range(q):
        L = vals[2 * i] - 1
        R = vals[2 * i + 1] - 1
        M = R - L + 1
        lo, hi = 0, M // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # check K = mid: min h over [L, L+mid-1] >= mid - M
            length = mid
            kk = length.bit_length() - 1
            row = table[kk]
            mn = row[L]
            v = row[L + length - (1 << kk)]
            if v < mn:
                mn = v
            if mn >= mid - M:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
