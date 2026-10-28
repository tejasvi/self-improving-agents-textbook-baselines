import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    size = [1] * (n + 2)
    lo = list(range(n + 2))   # left bound of run (valid at root)
    hi = list(range(n + 2))   # right bound of run (valid at root)
    color = list(range(n + 2))  # color of run (valid at root)
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
    pos = 2
    for _ in range(q):
        t = data[pos]
        if t == b'1':
            x = int(data[pos + 1])
            c = int(data[pos + 2])
            pos += 3
            r = find(x)
            o = color[r]
            if o == c:
                continue
            length = hi[r] - lo[r] + 1
            cnt[o] -= length
            cnt[c] += length
            color[r] = c
            L = lo[r]
            R = hi[r]
            if L > 1:
                lr = find(L - 1)
                if color[lr] == c:
                    r = union(r, lr)
            if R < n:
                rr = find(R + 1)
                if color[rr] == c:
                    r = union(r, rr)
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
