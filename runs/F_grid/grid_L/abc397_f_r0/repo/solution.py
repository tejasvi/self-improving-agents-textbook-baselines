import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    # 1-indexed positions
    A = [0] + a
    # L[i]: distinct count in A[1..i]
    L = [0] * (n + 1)
    seen = [False] * (n + 2)
    c = 0
    for i in range(1, n + 1):
        if not seen[A[i]]:
            seen[A[i]] = True
            c += 1
        L[i] = c
    # R[j]: distinct count in A[j+1..n]
    R = [0] * (n + 2)
    seen = [False] * (n + 2)
    c = 0
    for j in range(n, 0, -1):
        R[j] = c  # A[j+1..n] counted before adding A[j]
        if not seen[A[j]]:
            seen[A[j]] = True
            c += 1
    # nxt[p]: next occurrence index of A[p], or 0
    nxt = [0] * (n + 2)
    last = [0] * (n + 2)
    for p in range(n, 0, -1):
        nxt[p] = last[A[p]]
        last[A[p]] = p

    NEG = -(1 << 60)
    size = 1
    while size < n + 1:
        size *= 2
    mx = [NEG] * (2 * size)
    d = [0] * (2 * size)
    # leaf j holds f_1(j) + R[j] = L[j] + R[j], for 1 <= j <= n-1
    for j in range(1, n):
        mx[size + j] = L[j] + R[j]
    for i in range(size - 1, 0, -1):
        mx[i] = max(mx[2 * i], mx[2 * i + 1])

    def apply_range(l, r, v):
        # add v on [l, r)
        l += size
        r += size
        l0, r0 = l, r - 1
        while l < r:
            if l & 1:
                mx[l] += v
                d[l] += v
                l += 1
            if r & 1:
                r -= 1
                mx[r] += v
                d[r] += v
            l >>= 1
            r >>= 1
        i = l0 >> 1
        while i:
            mx[i] = max(mx[2 * i], mx[2 * i + 1]) + d[i]
            i >>= 1
        i = r0 >> 1
        while i:
            mx[i] = max(mx[2 * i], mx[2 * i + 1]) + d[i]
            i >>= 1

    def push_path(x):
        for h in range(size.bit_length() - 1, 0, -1):
            i = x >> h
            v = d[i]
            if v:
                for ch in (2 * i, 2 * i + 1):
                    mx[ch] += v
                    d[ch] += v
                d[i] = 0

    def query(l, r):
        # max on [l, r)
        l += size
        r += size
        push_path(l)
        push_path(r - 1)
        res = NEG
        while l < r:
            if l & 1:
                if mx[l] > res:
                    res = mx[l]
                l += 1
            if r & 1:
                r -= 1
                if mx[r] > res:
                    res = mx[r]
            l >>= 1
            r >>= 1
        return res

    best = 0
    # state currently s = 1; transition to s uses removal of position s-1
    for s in range(2, n):
        p = s - 1
        # remove position p: -1 on [p, n]
        apply_range(p, n + 1, -1)
        q = nxt[p]
        if q:
            apply_range(q, n + 1, 1)
        # j in [s, n-1]
        cand = L[s - 1] + query(s, n)
        if cand > best:
            best = cand
    print(best)

main()
