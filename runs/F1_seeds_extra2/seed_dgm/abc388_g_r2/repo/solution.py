import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    INF = 1 << 60
    # 0-indexed: nxt[i] = first j with 2*A[i] <= A[j]; h[i] = nxt[i] - i
    h = []
    for i in range(n):
        j = bisect_left(A, 2 * A[i])
        h.append(j - i if j < n else INF)
    # sparse table for range max
    table = [h]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        cur = [max(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)]
        table.append(cur)
        k += 1
    out = []
    pos = 2 + n
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        lo, hi = 0, (R - L + 1) // 2
        # find max K in [lo, hi] with feasible(K)
        while lo < hi:
            K = (lo + hi + 1) // 2
            # max h over [L, L+K-1]
            length = K
            lg = length.bit_length() - 1
            t = table[lg]
            m = max(t[L], t[L + K - (1 << lg)])
            # feasible iff m + L <= R - K + 1  (0-indexed)
            if m + L <= R - K + 1:
                lo = K
            else:
                hi = K - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
