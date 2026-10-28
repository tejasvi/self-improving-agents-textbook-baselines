import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n

    # d[j] = g(j) - j, where g(j) = first index k with A[k] >= 2*A[j]
    BIG = 10 ** 9
    d = [0] * n
    for j in range(n):
        g = bisect_left(A, 2 * A[j])
        if g >= n:
            g = BIG
        d[j] = g - j

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
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        length = R - L + 1
        # feasible(K): max_{j in [L, L+K-1]} d[j] <= length - K
        lo, hi = 0, length // 2
        while lo < hi:
            K = (lo + hi + 1) >> 1
            ln = K
            lv = ln.bit_length() - 1
            row = table[lv]
            m1 = row[L]
            m2 = row[L + K - (1 << lv)]
            mx = m1 if m1 > m2 else m2
            if mx <= length - K:
                lo = K
            else:
                hi = K - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
