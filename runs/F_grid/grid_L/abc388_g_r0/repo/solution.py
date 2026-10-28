import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    # r[i] = p(i) - i, where p(i) = first index with A >= 2*A[i]
    r = [bisect_left(A, 2 * a) - i for i, a in enumerate(A)]
    # sparse table for range max
    table = [r]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        cur = [max(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)]
        table.append(cur)
        j += 1

    def rmq(lo, hi):  # inclusive, lo <= hi
        k = (hi - lo + 1).bit_length() - 1
        t = table[k]
        a = t[lo]
        b = t[hi - (1 << k) + 1]
        return a if a > b else b

    out = []
    pos = 2 + n
    for _ in range(q):
        l = int(data[pos]) - 1
        rr = int(data[pos + 1]) - 1
        pos += 2
        length = rr - l + 1
        lo, hi = 0, length // 2  # find largest feasible K
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if rmq(l, l + mid - 1) <= length - mid:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
