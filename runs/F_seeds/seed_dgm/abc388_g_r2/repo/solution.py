import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    vals = data[2 + n:2 + n + 2 * q]

    # p[i]: first index j with A[j] >= 2*A[i]; g[i] = p[i] - i
    g = [bisect_left(A, 2 * A[i]) - i for i in range(n)]

    # sparse table for range max of g
    table = [g]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        cur = list(map(max, prev[:n - (1 << k) + 1], prev[half:half + n - (1 << k) + 1]))
        table.append(cur)
        k += 1

    out = []
    for qi in range(q):
        L = int(vals[2 * qi]) - 1
        R = int(vals[2 * qi + 1]) - 1
        length = R - L + 1
        # feasible(K): max g[L..L+K-1] <= length - K (monotone in K)
        lo, hi = 0, length // 2
        while lo < hi:
            m = (lo + hi + 1) // 2
            lg = (m).bit_length() - 1
            row = table[lg]
            r = max(row[L], row[L + m - (1 << lg)])
            if r <= length - m:
                lo = m
            else:
                hi = m - 1
        out.append(lo)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
