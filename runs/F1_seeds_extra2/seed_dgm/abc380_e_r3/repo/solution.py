import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
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

    def merge(a, b, c):
        # a, b roots of adjacent blocks; result gets color c
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        L[a] = min(L[a], L[b])
        R[a] = max(R[a], R[b])
        col[a] = c
        return a

    out = []
    pos = 2
    for _ in range(q):
        t = data[pos]
        if t == b'1':
            x = int(data[pos + 1]); c = int(data[pos + 2]); pos += 3
            root = find(x)
            d = col[root]
            if d == c:
                continue
            l = L[root]; r = R[root]
            sz = r - l + 1
            cnt[d] -= sz
            cnt[c] += sz
            col[root] = c
            if l > 1:
                lr = find(l - 1)
                if col[lr] == c:
                    root = merge(lr, root, c)
            if r < n:
                rr = find(r + 1)
                if col[rr] == c:
                    root = merge(root, rr, c)
        else:
            c = int(data[pos + 1]); pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
