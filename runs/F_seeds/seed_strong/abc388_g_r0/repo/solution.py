import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    q = int(data[1 + n])
    base = 2 + n

    # p[s] = first index j with A[j] >= 2*A[s]; val[s] = p[s] - s
    val = [bisect_left(A, 2 * A[s]) - s for s in range(n)]

    # sparse table for range max
    table = [val]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        table.append([x if x > y else y for x, y in zip(prev, prev[half:])])
        k += 1

    out = []
    for i in range(q):
        l = int(data[base + 2 * i]) - 1
        r = int(data[base + 2 * i + 1]) - 1
        lo = 0
        hi = (r - l + 1) // 2
        while lo < hi:
            m = (lo + hi + 1) >> 1
            # check range [l, l+m-1] max(val) <= r - m + 1 - l
            kk = (m).bit_length() - 1
            t = table[kk]
            a = t[l]
            b = t[l + m - (1 << kk)]
            if b > a:
                a = b
            if a <= r - m + 1 - l:
                lo = m
            else:
                hi = m - 1
        out.append(lo)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
