import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts: P1[i] = number of '1' in s[0:i] (1-indexed positions 1..i), same for P2
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    c1 = c2 = 0
    for i, ch in enumerate(s):
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        P1[i + 1] = c1
        P2[i + 1] = c2
    slashes = [i + 1 for i, ch in enumerate(s) if ch == '/']  # 1-indexed
    out = []
    pos = 3
    for _ in range(q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        lo = bisect_left(slashes, L)
        hi = bisect_left(slashes, R + 1)
        if lo >= hi:
            out.append(0)
            continue
        a = P1[L - 1]
        cR = P2[R]

        def xval(m):
            return P1[m - 1] - a

        def yval(m):
            return cR - P2[m]

        # first index j in [lo,hi) where xval >= yval (predicate monotone)
        l, h = lo, hi
        while l < h:
            mid = (l + h) >> 1
            m = slashes[mid]
            if xval(m) >= yval(m):
                h = mid
            else:
                l = mid + 1
        best = 0
        if l < hi:
            m = slashes[l]
            v = min(xval(m), yval(m))
            if v > best:
                best = v
        if l - 1 >= lo:
            m = slashes[l - 1]
            v = min(xval(m), yval(m))
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
