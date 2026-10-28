import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    # L[k]: distinct count in first k elements (k = 0..n)
    L = [0] * (n + 1)
    seen = set()
    for k in range(1, n + 1):
        seen.add(a[k - 1])
        L[k] = len(seen)
    # R[j]: distinct count in elements j+1..n (1-indexed j), suffix after position j
    R = [0] * (n + 2)
    seen = set()
    for j in range(n, 0, -1):
        R[j] = len(seen)  # seen holds elements j+1..n here
        seen.add(a[j - 1])

    size = 1
    while size < n + 1:
        size <<= 1
    LOG = size.bit_length() - 1
    NEG = -(1 << 60)
    t = [NEG] * (2 * size)
    d = [0] * (2 * size)
    # leaf index s (1..n) at position size + s; leaf 0 unused
    for s in range(1, n + 1):
        t[size + s] = L[s - 1]
    for i in range(size - 1, 0, -1):
        t[i] = max(t[2 * i], t[2 * i + 1])
    # exclude s = 1 (i must be >= 1)
    t[size + 1] = NEG
    for i in range(size - 1, 0, -1):
        t[i] = max(t[2 * i], t[2 * i + 1])

    def apply_range(l, r, v):  # [l, r)
        l += size
        r += size
        l0 = l
        r0 = r - 1
        while l < r:
            if l & 1:
                t[l] += v
                d[l] += v
                l += 1
            if r & 1:
                r -= 1
                t[r] += v
                d[r] += v
            l >>= 1
            r >>= 1
        i = l0 >> 1
        while i:
            t[i] = max(t[2 * i], t[2 * i + 1]) + d[i]
            i >>= 1
        i = r0 >> 1
        while i:
            t[i] = max(t[2 * i], t[2 * i + 1]) + d[i]
            i >>= 1

    def push(p):
        for s in range(LOG, 0, -1):
            i = p >> s
            v = d[i]
            if v:
                for c in (2 * i, 2 * i + 1):
                    t[c] += v
                    d[c] += v
                d[i] = 0

    def query(l, r):  # [l, r)
        l += size
        r += size
        push(l)
        push(r - 1)
        res = NEG
        while l < r:
            if l & 1:
                if t[l] > res:
                    res = t[l]
                l += 1
            if r & 1:
                r -= 1
                if t[r] > res:
                    res = t[r]
            l >>= 1
            r >>= 1
        return res

    last = {}
    best = 0
    for j in range(1, n + 1):
        v = a[j - 1]
        prev = last.get(v, 0)
        last[v] = j
        apply_range(prev + 1, j + 1, 1)  # s in (prev, j]
        if 2 <= j <= n - 1:
            cand = query(2, j + 1) + R[j]
            if cand > best:
                best = cand
    print(best)


main()
