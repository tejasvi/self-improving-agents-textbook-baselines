import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    L = list(range(n + 2))
    R = list(range(n + 2))
    col = list(range(n + 2))
    sz = [1] * (n + 2)
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b, c):
        # a, b roots of adjacent blocks; merge into one with color c
        if sz[a] < sz[b]:
            a, b = b, a
        parent[b] = a
        sz[a] += sz[b]
        L[a] = min(L[a], L[b])
        R[a] = max(R[a], R[b])
        col[a] = c
        return a

    pos = 2
    out = []
    for _ in range(q):
        t = data[pos]
        if t == b'1':
            x = int(data[pos + 1])
            c = int(data[pos + 2])
            pos += 3
            root = find(x)
            old = col[root]
            if old == c:
                continue
            s = sz[root]
            cnt[old] -= s
            cnt[c] += s
            col[root] = c
            # merge with left neighbor
            if L[root] > 1:
                lr = find(L[root] - 1)
                if col[lr] == c:
                    root = union(lr, root, c)
            # merge with right neighbor
            if R[root] < n:
                rr = find(R[root] + 1)
                if col[rr] == c:
                    root = union(root, rr, c)
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
