import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    s = data[2].decode()
    # prefix counts, 1-indexed: P1[i] = number of '1' in s[1..i]
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
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
        a = bisect_left(slashes, L)
        b = bisect_right(slashes, R)
        if a >= b:
            out.append(0)
            continue
        base1 = P1[L - 1]
        totalR2 = P2[R]
        # g(j) = ones in [L, m), h(j) = twos in (m, R]; g nondecreasing, h nonincreasing
        lo, hi = a, b
        while lo < hi:
            mid = (lo + hi) >> 1
            m = slashes[mid]
            g = P1[m - 1] - base1
            h = totalR2 - P2[m]
            if g >= h:
                hi = mid
            else:
                lo = mid + 1
        best = 0
        for j in (lo - 1, lo):
            if a <= j < b:
                m = slashes[j]
                g = P1[m - 1] - base1
                h = totalR2 - P2[m]
                v = g if g < h else h
                if v > best:
                    best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
