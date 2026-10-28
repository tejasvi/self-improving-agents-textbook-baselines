import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    a = [int(x) for x in a]

    # L[k] = distinct count of A[1..k]
    L = [0] * (n + 1)
    seen = set()
    for k in range(1, n + 1):
        seen.add(a[k - 1])
        L[k] = len(seen)

    # R[j] = distinct count of A[j+1..n]
    R = [0] * (n + 1)
    seen = set()
    for j in range(n, 0, -1):
        R[j] = len(seen)
        seen.add(a[j - 1])

    size = 1
    while size < n + 1:
        size <<= 1
    NEG = -10 ** 9
    t = [NEG] * (2 * size)
    d = [0] * size  # lazy for internal nodes

    def range_add(l, r, v):
        # add v on [l, r] inclusive, positions are 0..size-1
        l += size
        r += size + 1
        l0 = l
        r0 = r - 1
        while l < r:
            if l & 1:
                t[l] += v
                if l < size:
                    d[l] += v
                l += 1
            if r & 1:
                r -= 1
                t[r] += v
                if r < size:
                    d[r] += v
            l >>= 1
            r >>= 1
        i = l0 >> 1
        while i >= 1:
            x = t[2 * i]
            y = t[2 * i + 1]
            t[i] = (x if x > y else y) + d[i]
            i >>= 1
        i = r0 >> 1
        while i >= 1:
            x = t[2 * i]
            y = t[2 * i + 1]
            t[i] = (x if x > y else y) + d[i]
            i >>= 1

    BIG = 10 ** 9
    last = [0] * (n + 1)  # last occurrence index (1-based), 0 if none
    best = 0
    for j in range(1, n):
        v = a[j - 1]
        p = last[v]
        last[v] = j
        if j >= 2:
            # activate position s=j with value L[j-1] (D=0 initially)
            range_add(j, j, L[j - 1] + BIG)
        # D(s..j) increases by 1 for s in (p, j]
        range_add(p + 1, j, 1)
        if j >= 2:
            cand = t[1] + R[j]
            if cand > best:
                best = cand
    print(best)


main()
