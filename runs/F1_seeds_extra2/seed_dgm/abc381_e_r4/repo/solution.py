import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # 1-indexed prefix counts
    P1 = [0] * (n + 1)  # number of '1' in S[1..i]
    P2 = [0] * (n + 1)  # number of '2' in S[1..i]
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
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        x = P1[L - 1]
        y = P2[R]
        # g(m) = ones in [L,m) nondecreasing in m; h(m) = twos in (m,R] nonincreasing
        a, b = lo, hi
        while a < b:
            mid = (a + b) >> 1
            m = slashes[mid]
            g = P1[m - 1] - x
            h = y - P2[m]
            if g >= h:
                b = mid
            else:
                a = mid + 1
        best = 0
        if a < hi:
            m = slashes[a]
            g = P1[m - 1] - x
            h = y - P2[m]
            best = max(best, min(g, h))
        if a - 1 >= lo:
            m = slashes[a - 1]
            g = P1[m - 1] - x
            h = y - P2[m]
            best = max(best, min(g, h))
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
