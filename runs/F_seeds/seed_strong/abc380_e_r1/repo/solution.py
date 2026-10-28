import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    size = [1] * (n + 2)
    color = list(range(n + 2))
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

    out = []
    p = 2
    for _ in range(q):
        t = data[p]
        if t == b'1':
            x = int(data[p + 1]); c = int(data[p + 2]); p += 3
            r = find(x)
            old = color[r]
            if old == c:
                continue
            s = size[r]
            cnt[old] -= s
            cnt[c] += s
            color[r] = c
            l = lo[r]; h = hi[r]
            if l > 1:
                lr = find(l - 1)
                if color[lr] == c:
                    # merge lr and r
                    a, b = lr, r
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                    lo[a] = min(lo[a], lo[b]); hi[a] = max(hi[a], hi[b])
                    color[a] = c
                    r = a
            if h < n:
                rr = find(h + 1)
                if color[rr] == c:
                    a, b = r, rr
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                    lo[a] = min(lo[a], lo[b]); hi[a] = max(hi[a], hi[b])
                    color[a] = c
        else:
            c = int(data[p + 1]); p += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
