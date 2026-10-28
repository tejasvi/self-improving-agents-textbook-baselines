import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    vals = data[2 + n:2 + n + 2 * q]

    # f[i] = first index j with a[j] >= 2*a[i] (n if none); c[i] = i - f[i]
    # Pairing K smallest in [L, L+K-1] with K largest in [R-K+1, R] works iff
    # for all i in [L, L+K-1]: i - f[i] >= 0 relative, i.e. K <= M + min(c[i]).
    from bisect import bisect_left
    c = [i - bisect_left(a, 2 * a[i]) for i in range(n)]

    # sparse table for range minimum
    sp = [c]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        sp.append([min(x, y) for x, y in zip(prev, prev[half:])])
        k += 1

    out = []
    for qi in range(q):
        L = int(vals[2 * qi]) - 1
        R = int(vals[2 * qi + 1]) - 1
        M = R - L + 1
        lo, hi = 0, M // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            j = (mid).bit_length() - 1
            row = sp[j]
            mn = min(row[L], row[L + mid - (1 << j)])
            if mid <= M + mn:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
