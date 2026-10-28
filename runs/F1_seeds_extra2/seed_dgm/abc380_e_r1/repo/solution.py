import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    size = [1] * (n + 2)
    L = list(range(n + 2))
    R = list(range(n + 2))
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

    def union(a, b):
        # a, b are roots of adjacent blocks; merge them, return new root
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        L[a] = min(L[a], L[b])
        R[a] = max(R[a], R[b])
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
            s = size[r]
            cnt[old] -= s
            cnt[c] += s
            col[r] = c
            if L[r] > 1:
                l = find(L[r] - 1)
                if col[l] == c:
                    r = union(r, l)
            if R[r] < n:
                rr = find(R[r] + 1)
                if col[rr] == c:
                    r = union(r, rr)
            col[r] = c
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
