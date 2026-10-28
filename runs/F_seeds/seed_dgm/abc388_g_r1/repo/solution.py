import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n

    # g[i] = first index k with A[k] >= 2*A[i]; c[i] = g[i] - i
    c = [bisect_left(A, 2 * A[i]) - i for i in range(n)]

    # sparse table for range max of c
    table = [c]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        table.append([max(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)])
        j += 1

    out = []
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        lo = 0
        hi = (R - L + 1) // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # max of c over [L, L+mid-1]
            length = mid
            k = length.bit_length() - 1
            row = table[k]
            m = max(row[L], row[L + length - (1 << k)])
            if m + mid + L <= R + 1:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
