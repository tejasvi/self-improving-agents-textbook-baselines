import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    col = list(range(n + 2))
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1
    pos = 2
    out = []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        # a, b are distinct roots of adjacent runs; returns new root
        if lo[a] > lo[b]:
            a, b = b, a
        parent[b] = a
        if hi[b] > hi[a]:
            hi[a] = hi[b]
        return a

    for _ in range(q):
        if data[pos] == b'1':
            x = int(data[pos + 1]); c = int(data[pos + 2]); pos += 3
            r = find(x)
            old = col[r]
            if old == c:
                continue
            size = hi[r] - lo[r] + 1
            cnt[old] -= size
            cnt[c] += size
            col[r] = c
            l = lo[r]
            if l > 1:
                lr = find(l - 1)
                if col[lr] == c:
                    r = union(lr, r)
            h = hi[r]
            if h < n:
                rr = find(h + 1)
                if col[rr] == c:
                    r = union(r, rr)
            col[r] = c
        else:
            c = int(data[pos + 1]); pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
