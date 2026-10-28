import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # prefix counts
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
    # g(m) = P1[m] + P2[m] over slash positions is nondecreasing
    G = [P1[m] + P2[m] for m in slashes]
    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        lo = bisect_left(slashes, L)
        hi = bisect_right(slashes, R)
        if lo >= hi:
            out.append(0)
            continue
        a = P1[L - 1]
        b = P2[R]
        T = b + a
        i = bisect_left(G, T, lo, hi)
        best = 0
        for j in (i - 1, i):
            if lo <= j < hi:
                m = slashes[j]
                v = min(P1[m] - a, b - P2[m])
                if v > best:
                    best = v
        out.append(2 * best + 1)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
