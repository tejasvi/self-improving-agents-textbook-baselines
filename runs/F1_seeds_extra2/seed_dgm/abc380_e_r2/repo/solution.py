import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    # DSU over cells 1..n; each root represents a maximal run of equal color.
    parent = list(range(n + 2))
    size = [1] * (n + 2)
    lo = list(range(n + 2))   # left endpoint of run (valid at root)
    hi = list(range(n + 2))   # right endpoint of run (valid at root)
    col = list(range(n + 2))  # color of run (valid at root)
    cnt = [0] * (n + 2)       # cells per color
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        # a, b roots; merge, return new root
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        if lo[b] < lo[a]:
            lo[a] = lo[b]
        if hi[b] > hi[a]:
            hi[a] = hi[b]
        return a

    # initial merges: none (all colors distinct, adjacent runs differ)
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
            s = size[r]
            cnt[old] -= s
            cnt[c] += s
            col[r] = c
            L = lo[r]
            R = hi[r]
            if L > 1:
                lr = find(L - 1)
                if col[lr] == c:
                    r = union(lr, r)
            if R < n:
                rr = find(R + 1)
                if col[rr] == c:
                    r = union(r, rr)
            col[r] = c
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
