import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    M = n + 2
    SHIFT = M  # state = k << M | mask

    def enc(s):
        m = 0
        for i, c in enumerate(s):
            if c == 'W':
                m |= 1 << i
        return m

    start = (n << SHIFT) | enc(S)
    target = (n << SHIFT) | enc(T)
    if start == target:
        print(0)
        return

    seen = bytearray(1 << (SHIFT + 5))  # k <= n < 16
    seen[start] = 1
    cur = [start]
    dist = 0
    while cur:
        dist += 1
        nxt = []
        for st in cur:
            k = st >> SHIFT
            mask = st & ((1 << SHIFT) - 1)
            for x in range(M - 1):
                if x == k or x == k + 1 or x + 1 == k or x + 1 == k + 1:
                    continue
                bx = (mask >> x) & 1
                by = (mask >> (x + 1)) & 1
                nm = (mask & ~(3 << x)) | (bx << k) | (by << (k + 1))
                ns = (x << SHIFT) | nm
                if not seen[ns]:
                    if ns == target:
                        print(dist)
                        return
                    seen[ns] = 1
                    nxt.append(ns)
        cur = nxt
    print(-1)


main()
