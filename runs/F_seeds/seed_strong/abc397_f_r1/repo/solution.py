import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    # Lp[s] = distinct count of a[0..s-1]
    Lp = [0] * (n + 1)
    seen = set()
    for s in range(n):
        seen.add(a[s])
        Lp[s + 1] = len(seen)
    # Rs[k] = distinct count of a[k..n-1]
    Rs = [0] * (n + 1)
    seen = set()
    for k in range(n - 1, -1, -1):
        seen.add(a[k])
        Rs[k] = len(seen)

    # Segment tree over start positions s in [0, size).
    # Leaf s (1..n-1) holds Lp[s] + (distinct count of a[s..e]) once active (s <= e).
    # Inactive leaves hold very negative values. Values are max-with-lazy, no push.
    BIG = 1 << 30
    size = 1
    while size < n:
        size <<= 1
    t = [-(1 << 40)] * (2 * size)
    lz = [0] * (2 * size)
    for s in range(1, n):
        t[size + s] = Lp[s] - BIG
    for x in range(size - 1, 0, -1):
        c1 = t[2 * x]; c2 = t[2 * x + 1]
        t[x] = c1 if c1 > c2 else c2

    last = {}
    best = 0
    for e in range(1, n - 1):
        v = a[e]
        p = last.get(v, -1)
        last[v] = e
        # Leaf e becomes active: its value is Lp[e] + 1 (a[e] itself counted).
        # Starts s in [p+1, e] each gain one distinct element (includes e itself).
        # Range [p+1, e] with +1 and leaf e already has base Lp[e] -> total Lp[e]+1.
        t[size + e] += BIG  # activate leaf e (its path is recomputed below)
        l = p + 1 + size
        r = e + size + 1  # half-open [l, r)
        l0 = l
        r0 = r - 1
        while l < r:
            if l & 1:
                t[l] += 1
                if l < size:
                    lz[l] += 1
                l += 1
            if r & 1:
                r -= 1
                t[r] += 1
                if r < size:
                    lz[r] += 1
            l >>= 1
            r >>= 1
        # recompute ancestors of l0 and r0 together
        x = l0 >> 1
        y = r0 >> 1
        while x:
            if x == y:
                c1 = t[2 * x]; c2 = t[2 * x + 1]
                t[x] = (c1 if c1 > c2 else c2) + lz[x]
                x >>= 1
                y >>= 1
            else:
                c1 = t[2 * x]; c2 = t[2 * x + 1]
                t[x] = (c1 if c1 > c2 else c2) + lz[x]
                c1 = t[2 * y]; c2 = t[2 * y + 1]
                t[y] = (c1 if c1 > c2 else c2) + lz[y]
                x >>= 1
                y >>= 1
        cand = t[1] + Rs[e + 1]
        if cand > best:
            best = cand
    print(best)

main()
