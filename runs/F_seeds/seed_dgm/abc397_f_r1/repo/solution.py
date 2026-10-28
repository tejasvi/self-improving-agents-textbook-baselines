import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]

    # f[i]: distinct count in A[1..i]
    f = [0] * (n + 1)
    seen = set()
    for i in range(1, n + 1):
        seen.add(a[i - 1])
        f[i] = len(seen)

    # h[j]: distinct count in A[j+1..n]
    h = [0] * (n + 2)
    seen = set()
    for k in range(n, 0, -1):
        seen.add(a[k - 1])
        h[k - 1] = len(seen)

    # prev occurrence index (0 if none)
    last = {}
    prev = [0] * (n + 1)
    for j in range(1, n + 1):
        v = a[j - 1]
        prev[j] = last.get(v, 0)
        last[v] = j

    size = 1
    while size < n + 1:
        size *= 2
    NEG = -(1 << 40)
    # t[node] = max over subtree, including d[node] of this node and below
    # (lazy adds are not pushed down). True leaf value = t[leaf] + sum of d over ancestors.
    t = [NEG] * (2 * size)
    d = [0] * (2 * size)

    def range_add(lo, hi, v):
        l = lo + size
        r = hi + size + 1
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

    def activate(pos, val):
        p = pos + size
        s = 0
        q = p >> 1
        while q:
            s += d[q]
            q >>= 1
        t[p] = val - s
        q = p >> 1
        while q:
            t[q] = max(t[2 * q], t[2 * q + 1]) + d[q]
            q >>= 1

    best = NEG
    # right end of middle segment j in [2, n-1]; left end i in [1, j-1]
    for j in range(2, n):
        activate(j - 1, f[j - 1])
        lo = prev[j] if prev[j] >= 1 else 1
        range_add(lo, j - 1, 1)
        cand = t[1] + h[j]
        if cand > best:
            best = cand
    print(best)


main()
