import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    color = list(range(n + 2))
    size = [1] * (n + 2)
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

    def union(a, b):
        # a, b are roots; returns new root
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        if lo[b] < lo[a]:
            lo[a] = lo[b]
        if hi[b] > hi[a]:
            hi[a] = hi[b]
        return a

    out = []
    idx = 2
    for _ in range(q):
        t = data[idx]
        if t == b'1':
            x = int(data[idx + 1]); c = int(data[idx + 2]); idx += 3
            r = find(x)
            d = color[r]
            if d == c:
                continue
            length = hi[r] - lo[r] + 1
            cnt[d] -= length
            cnt[c] += length
            color[r] = c
            # merge with left neighbor run
            if lo[r] > 1:
                lr = find(lo[r] - 1)
                if color[lr] == c:
                    r = union(r, lr)
                    color[r] = c
            if hi[r] < n:
                rr = find(hi[r] + 1)
                if color[rr] == c:
                    r = union(r, rr)
                    color[r] = c
        else:
            c = int(data[idx + 1]); idx += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
