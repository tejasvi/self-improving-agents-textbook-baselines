import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts: P1[i] = number of '1' in s[1..i], P2[i] = number of '2' in s[1..i]
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    slashes = []
    c1 = c2 = 0
    for i, ch in enumerate(s, 1):
        if ch == '1':
            c1 += 1
        elif ch == '2':
            c2 += 1
        elif ch == '/':
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
        base1 = P1[L - 1]
        total2 = P2[R]
        # f(m) = P1[m-1] - base1 (ones in [L, m)), g(m) = total2 - P2[m] (twos in (m, R])
        # f(m) - g(m) = P1[m-1] + P2[m] - (base1 + total2) is nondecreasing in m
        target = base1 + total2
        a, b = lo, hi
        while a < b:
            mid = (a + b) >> 1
            m = slashes[mid]
            if P1[m - 1] + P2[m] >= target:
                b = mid
            else:
                a = mid + 1
        best = 0
        for j in (a - 1, a):
            if lo <= j < hi:
                m = slashes[j]
                f = P1[m - 1] - base1
                g = total2 - P2[m]
                v = f if f < g else g
                if v > best:
                    best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
