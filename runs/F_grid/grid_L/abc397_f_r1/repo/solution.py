import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [0] + [int(x) for x in data[1:1 + n]]  # 1-indexed

    # L[i]: distinct count in a[1..i]
    L = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(1, n + 1):
        if not seen[a[i]]:
            seen[a[i]] = True
            cnt += 1
        L[i] = cnt

    # R[j]: distinct count in a[j+1..n]
    R = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for j in range(n, 0, -1):
        # R[j] currently should be distinct count of a[j+1..n]
        R[j] = cnt
        if not seen[a[j]]:
            seen[a[j]] = True
            cnt += 1

    # Segment tree over positions i in [1, n-1] (split point i).
    # Value at i: L[i] + distinct(a[i+1..j]) for current j; only i <= j-1 active.
    # Non-lazy-propagation: node value = max(children) + add[node].
    NEG = -(1 << 40)
    size = 1
    while size < n + 1:
        size *= 2
    t = [NEG] * (2 * size)
    add = [0] * (2 * size)

    def pull_up(x):
        x >>= 1
        while x >= 1:
            l = t[2 * x]
            r = t[2 * x + 1]
            t[x] = (l if l > r else r) + add[x]
            x >>= 1

    def range_add(lo, hi):  # inclusive
        l = lo + size
        r = hi + size + 1
        l0, r0 = l, r - 1
        while l < r:
            if l & 1:
                t[l] += 1
                add[l] += 1
                l += 1
            if r & 1:
                r -= 1
                t[r] += 1
                add[r] += 1
            l >>= 1
            r >>= 1
        pull_up(l0)
        pull_up(r0)

    last = [0] * (n + 1)
    ans = 0
    for j in range(1, n + 1):
        if j >= 2:
            # activate split point i = j-1 with value L[j-1]
            x = (j - 1) + size
            s_anc = 0
            y = x >> 1
            while y >= 1:
                s_anc += add[y]
                y >>= 1
            t[x] = L[j - 1] - s_anc
            pull_up(x)
        p = last[a[j]]
        last[a[j]] = j
        lo = p if p >= 1 else 1
        if lo <= j - 1:
            range_add(lo, j - 1)
        if 2 <= j <= n - 1:
            cand = t[1] + R[j]
            if cand > ans:
                ans = cand
    print(ans)


main()
