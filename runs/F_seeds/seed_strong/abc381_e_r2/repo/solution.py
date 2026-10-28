import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # 1-indexed prefix counts
    p1 = [0] * (n + 1)  # count of '1' in s[1..i]
    p2 = [0] * (n + 1)  # count of '2' in s[1..i]
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
        i0 = bisect_left(slashes, L)
        i1 = bisect_left(slashes, R + 1) - 1
        if i0 > i1:
            out.append(0)
            continue
        x = p1[L - 1]
        Y = p2[R]
        # predicate(j): p1[m-1]-x >= Y-p2[m], monotone (false...true)
        lo, hi = i0, i1 + 1
        while lo < hi:
            mid = (lo + hi) >> 1
            m = slashes[mid]
            if p1[m - 1] - x >= Y - p2[m]:
                hi = mid
            else:
                lo = mid + 1
        t = lo
        best = 0
        if t <= i1:
            m = slashes[t]
            v = Y - p2[m]
            if v > best:
                best = v
        if t - 1 >= i0:
            m = slashes[t - 1]
            v = p1[m - 1] - x
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
