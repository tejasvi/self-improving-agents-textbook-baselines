import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    p1 = [0] * (n + 1)
    p2 = [0] * (n + 1)
    slashes = []
    c1 = c2 = 0
    for i, ch in enumerate(s, 1):
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        else:
            slashes.append(i)
        p1[i] = c1
        p2[i] = c2
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R) - 1
        if lo > hi:
            out.append(0)
            continue
        x = p1[L - 1]
        y = p2[R]

        def val(j):
            m = slashes[j]
            a = p1[m - 1] - x
            b = y - p2[m]
            return a if a < b else b

        # smallest j in [lo,hi] with left >= right
        l, r = lo, hi + 1
        while l < r:
            mid = (l + r) >> 1
            m = slashes[mid]
            if p1[m - 1] - x >= y - p2[m]:
                r = mid
            else:
                l = mid + 1
        best = 0
        if l <= hi:
            best = max(best, val(l))
        if l - 1 >= lo:
            best = max(best, val(l - 1))
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
