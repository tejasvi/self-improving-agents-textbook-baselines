import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts
    A = [0] * (n + 1)  # count of '1' in s[1..i]
    B = [0] * (n + 1)  # count of '2' in s[1..i]
    for i, ch in enumerate(s, 1):
        A[i] = A[i - 1] + (ch == '1')
        B[i] = B[i - 1] + (ch == '2')
    slashes = [i for i, ch in enumerate(s, 1) if ch == '/']
    out = []
    pos = 3
    for _ in range(q):
        L = int(data[pos])
        R = int(data[pos + 1])
        pos += 2
        i0 = bisect_left(slashes, L)
        i1 = bisect_right(slashes, R) - 1
        if i0 > i1:
            out.append(0)
            continue
        AL = A[L - 1]
        BR = B[R]
        # first index j in [i0, i1] with f(m) > g(m); f-g nondecreasing
        lo, hi = i0, i1 + 1
        while lo < hi:
            mid = (lo + hi) >> 1
            m = slashes[mid]
            f = A[m - 1] - AL
            g = BR - B[m]
            if f > g:
                hi = mid
            else:
                lo = mid + 1
        best = 0
        j = lo
        if j - 1 >= i0:
            m = slashes[j - 1]
            f = A[m - 1] - AL
            g = BR - B[m]
            best = max(best, min(f, g))
        if j <= i1:
            m = slashes[j]
            f = A[m - 1] - AL
            g = BR - B[m]
            best = max(best, min(f, g))
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
