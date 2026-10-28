import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]

    # pre[i]: distinct count of a[0..i]
    seen = set()
    pre = [0] * n
    for i in range(n):
        seen.add(a[i])
        pre[i] = len(seen)

    # suf[k]: distinct count of a[k..n-1]
    seen = set()
    suf = [0] * (n + 1)
    for k in range(n - 1, -1, -1):
        seen.add(a[k])
        suf[k] = len(seen)

    # prev[p]: previous index with same value, or -1
    last = {}
    prev = [-1] * n
    for p in range(n):
        v = a[p]
        prev[p] = last.get(v, -1)
        last[v] = p

    NEG = -(10 ** 18)
    size = 1
    while size < n:
        size *= 2
    t = [NEG] * (2 * size)  # t[p] = max over subtree, including d[p]
    d = [0] * size          # pending add for internal node p (applies to whole subtree)

    def rebuild(x):
        p = x >> 1
        while p >= 1:
            a1 = t[2 * p]
            b1 = t[2 * p + 1]
            t[p] = (a1 if a1 > b1 else b1) + d[p]
            p >>= 1

    def range_add(l, r):
        # +1 on leaves [l, r] inclusive
        l += size
        r += size + 1
        l0 = l
        r0 = r - 1
        while l < r:
            if l & 1:
                t[l] += 1
                if l < size:
                    d[l] += 1
                l += 1
            if r & 1:
                r -= 1
                t[r] += 1
                if r < size:
                    d[r] += 1
            l >>= 1
            r >>= 1
        rebuild(l0)
        rebuild(r0)

    def activate(k, value):
        leaf = k + size
        s = 0
        p = leaf >> 1
        while p >= 1:
            s += d[p]
            p >>= 1
        t[leaf] = value - s
        rebuild(leaf)

    best = 0
    for j in range(1, n - 1):
        # left end i = j-1 becomes valid: prefix a[0..j-1], middle starts empty
        activate(j - 1, pre[j - 1])
        # middle a[i+1..j]: adding a[j] gives +1 for i in [prev[j], j-1]
        lo = prev[j] if prev[j] > 0 else 0
        range_add(lo, j - 1)
        cand = t[1] + suf[j + 1]
        if cand > best:
            best = cand
    print(best)


main()
