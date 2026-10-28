import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    # 1-indexed values a[1..n]
    A = [0] + a
    # L[i] = distinct count in A[1..i]
    L = [0] * (n + 1)
    seen = set()
    for i in range(1, n + 1):
        seen.add(A[i])
        L[i] = len(seen)
    # R[j] = distinct count in A[j+1..n]
    R = [0] * (n + 1)
    seen = set()
    for j in range(n, 0, -1):
        # R[j-1] = distinct in A[j..n]
        seen.add(A[j])
        R[j - 1] = len(seen)
    # nxt[l] = next index with same value, or n
    nxt = [n] * (n + 2)
    last = {}
    for i in range(n, 0, -1):
        nxt[i] = last.get(A[i], n)
        last[A[i]] = i

    size = 1
    while size < n + 1:
        size *= 2
    BIG = 10 ** 9
    t = [-BIG] * (2 * size)   # max over subtree including adds at this node
    d = [0] * (2 * size)      # pending add at internal nodes
    for j in range(1, n):
        t[size + j] = R[j] - BIG
    for p in range(size - 1, 0, -1):
        t[p] = max(t[2 * p], t[2 * p + 1])

    def add(lo, hi, v):
        # add v on half-open [lo, hi)
        l = lo + size
        r = hi + size
        l0, r0 = l, r - 1
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
        # rebuild ancestors of l0 and r0
        p = l0 >> 1
        while p >= 1:
            t[p] = max(t[2 * p], t[2 * p + 1]) + d[p]
            p >>= 1
        p = r0 >> 1
        while p >= 1:
            t[p] = max(t[2 * p], t[2 * p + 1]) + d[p]
            p >>= 1

    best = 0
    for l in range(n - 1, 1, -1):
        # activate position l and add contribution of element A[l]
        add(l, l + 1, BIG)
        add(l, nxt[l], 1)
        cand = L[l - 1] + t[1]
        if cand > best:
            best = cand
    print(best)

main()
