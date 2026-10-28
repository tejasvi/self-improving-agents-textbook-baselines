import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    q = int(data[1 + n])
    pos = 2 + n

    # f[x] = smallest j with a[j] >= 2*a[x]; h[x] = f[x] - x
    h = [bisect_left(a, 2 * a[x]) - x for x in range(n)]

    # sparse table for range maximum of h
    table = [h]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        table.append(list(map(max, prev[:-half], prev[half:])))
        k += 1

    out = []
    for _ in range(q):
        l = int(data[pos]) - 1
        r = int(data[pos + 1]) - 1
        pos += 2
        lo = 0
        hi = (r - l + 1) // 2
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            # max of h over [l, l+mid)
            j = mid.bit_length() - 1
            t = table[j]
            m = t[l]
            v = t[l + mid - (1 << j)]
            if v > m:
                m = v
            if m <= r - mid + 1 - l:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
