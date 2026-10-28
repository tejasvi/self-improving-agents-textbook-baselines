import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    INF = 10 ** 9
    # g[x] = smallest index j with A[j] >= 2*A[x]; h[x] = g[x] - x
    h = [0] * n
    for x in range(n):
        g = bisect_left(A, 2 * A[x])
        if g >= n:
            g = INF
        h[x] = g - x
    # sparse table for range max of h
    table = [h]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        cur = [max(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)]
        table.append(cur)
        j += 1
    out = []
    pos = 2 + n
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        lo, hi = 0, (R - L + 1) // 2
        # find largest K in [0, hi] feasible
        while lo < hi:
            K = (lo + hi + 1) >> 1
            # max h over [L, L+K-1]
            length = K
            k = length.bit_length() - 1
            row = table[k]
            m1 = row[L]
            m2 = row[L + K - (1 << k)]
            mx = m1 if m1 > m2 else m2
            if mx <= R - K + 1 - L:
                lo = K
            else:
                hi = K - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
