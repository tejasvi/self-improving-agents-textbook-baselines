import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    s = data[2].decode()
    # prefix counts, 1-indexed: P1[i] = #'1' in s[1..i]
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    slashes = []
    for i, c in enumerate(s, 1):
        P1[i] = P1[i - 1] + (c == '1')
        P2[i] = P2[i - 1] + (c == '2')
        if c == '/':
            slashes.append(i)
    G = [P1[p] + P2[p] for p in slashes]
    out = []
    pos = 3
    for _ in range(q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        T = P1[L - 1] + P2[R]
        idx = bisect_right(G, T, lo, hi)
        best = 0
        if idx > lo:
            p1 = slashes[idx - 1]
            u = P1[p1] - P1[L - 1]
            if u > best:
                best = u
        if idx < hi:
            p2 = slashes[idx]
            v = P2[R] - P2[p2]
            if v > best:
                best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
