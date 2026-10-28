import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    # d[j] = p(j) - j, where p(j) = first index k with A[k] >= 2*A[j] (n if none)
    d = [0] * n
    for j in range(n):
        d[j] = bisect_left(A, 2 * A[j]) - j
    # sparse table for range max
    table = [d]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        cur = [max(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)]
        table.append(cur)
        k += 1
    out = []
    idx = 2 + n
    for _ in range(q):
        L = int(data[idx]) - 1
        R = int(data[idx + 1]) - 1
        idx += 2
        lo, hi = 0, (R - L + 1) // 2
        # find max K in [0, hi] feasible; feasibility monotone
        while lo < hi:
            K = (lo + hi + 1) >> 1
            # max d over [L, L+K-1]
            ln = K
            lg = ln.bit_length() - 1
            t = table[lg]
            m = t[L] if t[L] > t[L + ln - (1 << lg)] else t[L + ln - (1 << lg)]
            if m <= R - K + 1 - L:
                lo = K
            else:
                hi = K - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
