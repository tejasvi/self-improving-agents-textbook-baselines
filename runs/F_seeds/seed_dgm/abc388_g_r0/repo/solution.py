import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n

    # f[p] = first index j with A[j] >= 2*A[p]
    v = [bisect_left(A, 2 * A[p]) - p for p in range(n)]

    # sparse table for range max of v
    table = [v]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        table.append([max(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)])
        k += 1

    out = []
    for _ in range(q):
        l = int(data[pos]) - 1
        r = int(data[pos + 1]) - 1
        pos += 2
        length = r - l + 1
        lo, hi = 0, length // 2
        while lo < hi:
            K = (lo + hi + 1) // 2
            # max of v over [l, l+K-1]
            j = (K).bit_length() - 1
            t = table[j]
            m = max(t[l], t[l + K - (1 << j)])
            if m + K <= length:
                lo = K
            else:
                hi = K - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
