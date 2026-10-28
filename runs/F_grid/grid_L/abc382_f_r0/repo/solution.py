import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); N = int(data[2])
    bars = []
    idx = 3
    for i in range(N):
        r = int(data[idx]); c = int(data[idx + 1]); l = int(data[idx + 2])
        idx += 3
        bars.append((r, c, l))

    # Lazy segment tree over columns 1..W: range assign, range min.
    size = 1
    while size < W:
        size *= 2
    INF = H + 1
    mn = [INF] * (2 * size)
    lz = [-1] * (2 * size)  # -1 = no pending assignment

    def apply(node, v):
        mn[node] = v
        lz[node] = v

    def push(node):
        if lz[node] != -1:
            apply(2 * node, lz[node])
            apply(2 * node + 1, lz[node])
            lz[node] = -1

    def query(node, nl, nr, l, r):
        if r < nl or nr < l:
            return INF
        if l <= nl and nr <= r:
            return mn[node]
        push(node)
        mid = (nl + nr) // 2
        a = query(2 * node, nl, mid, l, r)
        b = query(2 * node + 1, mid + 1, nr, l, r)
        return a if a < b else b

    def update(node, nl, nr, l, r, v):
        if r < nl or nr < l:
            return
        if l <= nl and nr <= r:
            apply(node, v)
            return
        push(node)
        mid = (nl + nr) // 2
        update(2 * node, nl, mid, l, r, v)
        update(2 * node + 1, mid + 1, nr, l, r, v)
        a = mn[2 * node]; b = mn[2 * node + 1]
        mn[node] = a if a < b else b

    order = sorted(range(N), key=lambda i: -bars[i][0])
    ans = [0] * N
    for i in order:
        r, c, l = bars[i]
        lo = c - 1  # 0-indexed columns
        hi = c + l - 2
        top = query(1, 0, size - 1, lo, hi)
        nr = top - 1
        ans[i] = nr
        update(1, 0, size - 1, lo, hi, nr)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
