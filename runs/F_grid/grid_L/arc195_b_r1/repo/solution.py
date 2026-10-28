import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    B = [int(x) for x in data[1 + n:1 + 2 * n]]

    K = [a for a in A if a != -1]
    x = n - len(K)                     # free slots in A
    bk = [b for b in B if b != -1]
    M = len(bk)                        # positions with known B
    t = M - x                          # minimum number of matches needed
    if t <= 0:
        print("Yes")
        return

    L = max(max(K, default=0), max(bk, default=0))
    cA = Counter(K)
    cB = Counter(bk)

    # matched(S) = sum over pairs (w, v) with w + v = S of min(cB[w], cA[v])
    acc = {}
    for w, cw in cB.items():
        for v, cv in cA.items():
            s = w + v
            if s >= L:
                acc[s] = acc.get(s, 0) + (cw if cw < cv else cv)
    best = max(acc.values(), default=0)
    print("Yes" if best >= t else "No")


main()
