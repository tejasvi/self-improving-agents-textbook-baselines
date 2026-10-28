import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    bars = []
    idx = 3
    for i in range(N):
        r = int(data[idx]); c = int(data[idx + 1]); l = int(data[idx + 2])
        idx += 3
        bars.append((r, c, l, i))

    # Process bars from lowest initial row to highest.
    order = sorted(range(N), key=lambda i: -bars[i][0])

    size = 1
    LOG = 0
    while size < W:
        size *= 2
        LOG += 1
    INF = H + 1
    mn = [INF] * (2 * size)
    lz = [-1] * (2 * size)

    def apply(node, v):
        mn[node] = v
        lz[node] = v

    def push(node):
        v = lz[node]
        if v != -1:
            apply(2 * node, v)
            apply(2 * node + 1, v)
            lz[node] = -1

    def query(l, r):  # [l, r)
        l += size
        r += size
        for h in range(LOG, 0, -1):
            if ((l >> h) << h) != l:
                push(l >> h)
            if ((r >> h) << h) != r:
                push((r - 1) >> h)
        res = INF * 4
        while l < r:
            if l & 1:
                if mn[l] < res:
                    res = mn[l]
                l += 1
            if r & 1:
                r -= 1
                if mn[r] < res:
                    res = mn[r]
            l >>= 1
            r >>= 1
        return res

    def update(l, r, v):  # [l, r) assign v
        l += size
        r += size
        l0, r0 = l, r
        for h in range(LOG, 0, -1):
            if ((l0 >> h) << h) != l0:
                push(l0 >> h)
            if ((r0 >> h) << h) != r0:
                push((r0 - 1) >> h)
        while l < r:
            if l & 1:
                apply(l, v)
                l += 1
            if r & 1:
                r -= 1
                apply(r, v)
            l >>= 1
            r >>= 1
        for h in range(1, LOG + 1):
            p = l0 >> h
            if ((l0 >> h) << h) != l0:
                mn[p] = min(mn[2 * p], mn[2 * p + 1])
            p = (r0 - 1) >> h
            if ((r0 >> h) << h) != r0:
                mn[p] = min(mn[2 * p], mn[2 * p + 1])

    ans = [0] * N
    for i in order:
        r0, c, l, _ = bars[i]
        lo = c - 1
        hi = c - 1 + l
        m = query(lo, hi)
        row = min(H, m - 1)
        ans[i] = row
        update(lo, hi, row)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
