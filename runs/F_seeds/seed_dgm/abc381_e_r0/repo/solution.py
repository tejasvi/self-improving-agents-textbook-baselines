import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts
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
        base = p1[L - 1]
        total2 = p2[R]
        # first index k in [lo, hi] with ones_before - base > twos_after
        a, b = lo, hi + 1
        while a < b:
            mid = (a + b) >> 1
            m = slashes[mid]
            if p1[m] - base > total2 - p2[m]:
                b = mid
            else:
                a = mid + 1
        k = a
        best = 0
        if k - 1 >= lo:
            m = slashes[k - 1]
            v = min(p1[m] - base, total2 - p2[m])
            if v > best:
                best = v
        if k <= hi:
            m = slashes[k]
            v = min(p1[m] - base, total2 - p2[m])
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
