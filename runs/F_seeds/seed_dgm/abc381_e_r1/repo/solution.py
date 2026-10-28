import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts (1-indexed)
    P1 = [0] * (n + 1)  # count of '1'
    P2 = [0] * (n + 1)  # count of '2'
    slashes = []
    c1 = c2 = 0
    for i, ch in enumerate(s, 1):
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        else:
            slashes.append(i)
        P1[i] = c1
        P2[i] = c2

    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        p1L = P1[L - 1]
        p2R = P2[R]
        # smallest i in [lo, hi) with A(i) >= B(i)
        a, b = lo, hi
        while a < b:
            mid = (a + b) >> 1
            m = slashes[mid]
            A = P1[m - 1] - p1L
            B = p2R - P2[m]
            if A >= B:
                b = mid
            else:
                a = mid + 1
        i = a
        best = 0
        if i < hi:
            m = slashes[i]
            best = max(best, p2R - P2[m])  # min is B here
        if i - 1 >= lo:
            m = slashes[i - 1]
            best = max(best, P1[m - 1] - p1L)  # min is A here
        out.append(2 * best + 1)

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
