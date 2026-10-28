import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # L[a] = distinct count in A[0..a-1], for a = 0..n
    L = [0] * (n + 1)
    seen = [False] * (n + 2)
    cnt = 0
    for a in range(n):
        if not seen[A[a]]:
            seen[A[a]] = True
            cnt += 1
        L[a + 1] = cnt

    # R[j] = distinct count in A[j+1..n-1]
    R = [0] * n
    seen = [False] * (n + 2)
    cnt = 0
    for j in range(n - 1, -1, -1):
        R[j] = cnt
        if not seen[A[j]]:
            seen[A[j]] = True
            cnt += 1

    # Segment tree over a in [0, n]:
    # value[a] = L[a] + distinct(A[a..j]) for a <= j.
    size = 1
    h = 0
    while size < n + 1:
        size <<= 1
        h += 1
    NEG = -(1 << 60)
    t = [NEG] * (2 * size)
    d = [0] * (2 * size)
    for a in range(n + 1):
        t[size + a] = L[a]
    for node in range(size - 1, 0, -1):
        t[node] = max(t[2 * node], t[2 * node + 1])

    def apply(node, v):
        t[node] += v
        if node < size:
            d[node] += v

    def build(node):
        while node > 1:
            node >>= 1
            a1 = t[2 * node]
            a2 = t[2 * node + 1]
            t[node] = (a1 if a1 > a2 else a2) + d[node]

    def push(node):
        for s in range(h, 0, -1):
            i = node >> s
            v = d[i]
            if v:
                apply(2 * i, v)
                apply(2 * i + 1, v)
                d[i] = 0

    def inc(l, r, v):
        # add v on [l, r)
        l += size
        r += size
        l0, r0 = l, r - 1
        while l < r:
            if l & 1:
                apply(l, v)
                l += 1
            if r & 1:
                r -= 1
                apply(r, v)
            l >>= 1
            r >>= 1
        build(l0)
        build(r0)

    def query(l, r):
        # max on [l, r)
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
    best = NEG
    # j is the inclusive end of the middle segment; third segment is A[j+1..]
    for j in range(n - 1):
        p = last.get(A[j], -1)
        last[A[j]] = j
        # distinct(A[a..j]) increases by 1 for a in [p+1, j]
        inc(p + 1, j + 1, 1)
        if j >= 1:
            # first segment is A[0..a-1], a in [1, j]
            cand = query(1, j + 1) + R[j]
            if cand > best:
                best = cand
    print(best)


main()
