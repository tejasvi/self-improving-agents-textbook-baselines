import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    col = list(range(n + 2))
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def merge(a, b, c):
        # a, b are roots of adjacent segments with same color c; returns new root
        if lo[a] > lo[b]:
            a, b = b, a
        # a is left segment
        parent[b] = a
        hi[a] = hi[b]
        col[a] = c
        return a

    out = []
    pos = 2
    for _ in range(q):
        t = data[pos]
        if t == b'1':
            x = int(data[pos + 1])
            c = int(data[pos + 2])
            pos += 3
            r = find(x)
            old = col[r]
            if old == c:
                continue
            size = hi[r] - lo[r] + 1
            cnt[old] -= size
            cnt[c] += size
            col[r] = c
            if lo[r] > 1:
                l = find(lo[r] - 1)
                if col[l] == c:
                    r = merge(l, r, c)
            if hi[r] < n:
                rr = find(hi[r] + 1)
                if col[rr] == c:
                    r = merge(r, rr, c)
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
