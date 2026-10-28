import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n

    # c[p] = (first index j with A[j] >= 2*A[p]) - p
    c = [bisect_left(A, 2 * A[p]) - p for p in range(n)]

    # sparse table for range max of c
    table = [c]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        table.append(list(map(max, prev[:len(prev) - half], prev[half:])))
        k += 1

    out = []
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        lo = 0
        hi = (R - L + 1) // 2
        while lo < hi:
            K = (lo + hi + 1) // 2
            kk = K.bit_length() - 1
            row = table[kk]
            mx = max(row[L], row[L + K - (1 << kk)])
            if mx <= R - L - K + 1:
                lo = K
            else:
                hi = K - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
