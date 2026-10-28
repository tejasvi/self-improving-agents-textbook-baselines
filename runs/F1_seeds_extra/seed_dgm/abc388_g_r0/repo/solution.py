import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n

    # nxt[p] = first index j with A[j] >= 2*A[p] (n if none)
    d = [bisect_left(A, 2 * A[p]) - p for p in range(n)]

    # sparse table for range max of d
    sp = [d]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        h = 1 << (k - 1)
        sp.append(list(map(max, prev[:len(prev) - h], prev[h:])))
        k += 1

    out = []
    for _ in range(q):
        l = int(data[pos]) - 1
        r = int(data[pos + 1]) - 1
        pos += 2
        length = r - l + 1
        lo, hi = 0, length // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # max d over [l, l+mid-1]
            j = (mid).bit_length() - 1
            row = sp[j]
            m = max(row[l], row[l + mid - (1 << j)])
            if m + mid <= length:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
