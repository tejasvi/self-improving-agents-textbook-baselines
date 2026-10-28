import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    # L[k] = distinct count of A_1..A_k ; R[k] = distinct count of A_k..A_n
    L = [0] * (n + 2)
    seen = set()
    for k in range(1, n + 1):
        seen.add(A[k - 1])
        L[k] = len(seen)
    R = [0] * (n + 2)
    seen = set()
    for k in range(n, 0, -1):
        seen.add(A[k - 1])
        R[k] = len(seen)

    # Segment tree over split points i. When middle end is j, active leaf i
    # (1 <= i <= j-1) holds L[i] + distinct(i+1..j); inactive leaves are NEG.
    # t[v] = max over subtree including adds at v and below; d[v] = pending add at v.
    NEG = -(1 << 40)
    size = 1
    while size < n + 1:
        size *= 2
    t = [NEG] * (2 * size)
    d = [0] * (2 * size)

    last = {}
    best = 0
    for j in range(1, n + 1):
        a = A[j - 1]
        p = last.get(a, 0)
        last[a] = j
        # activate leaf j-1 (ancestors have no pending adds: no range touched it yet)
        leaf = size + j - 1
        if j >= 2:
            t[leaf] = L[j - 1]
        # splits i in [p, j-1] gain 1
        l = p + size
        r = leaf + 1
        l0 = l
        r0 = leaf
        while l < r:
            if l & 1:
                t[l] += 1
                d[l] += 1
                l += 1
            if r & 1:
                r -= 1
                t[r] += 1
                d[r] += 1
            l >>= 1
            r >>= 1
        v = l0 >> 1
        w = r0 >> 1
        while v != w:
            x = t[2 * v]; y = t[2 * v + 1]
            t[v] = (x if x > y else y) + d[v]
            x = t[2 * w]; y = t[2 * w + 1]
            t[w] = (x if x > y else y) + d[w]
            v >>= 1
            w >>= 1
        while v:
            x = t[2 * v]; y = t[2 * v + 1]
            t[v] = (x if x > y else y) + d[v]
            v >>= 1
        if 2 <= j <= n - 1:
            cand = t[1] + R[j + 1]
            if cand > best:
                best = cand
    print(best)

main()
