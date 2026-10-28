import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts, 1-indexed: P1[i] = number of '1' in s[1..i], P2 similarly
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    for i in range(1, n + 1):
        c = s[i - 1]
        P1[i] = P1[i - 1] + (c == '1')
        P2[i] = P2[i - 1] + (c == '2')
    slashes = []
    F = []  # F[k] = P1[m-1] + P2[m] for slash m = slashes[k]; nondecreasing
    for i in range(1, n + 1):
        if s[i - 1] == '/':
            slashes.append(i)
            F.append(P1[i - 1] + P2[i])
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        K = P2[R] + P1[L - 1]
        j = bisect_left(F, K, lo, hi)
        best = 0
        for c in (j - 1, j):
            if lo <= c < hi:
                m = slashes[c]
                g = P1[m - 1] - P1[L - 1]
                h = P2[R] - P2[m]
                v = g if g < h else h
                if v > best:
                    best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
