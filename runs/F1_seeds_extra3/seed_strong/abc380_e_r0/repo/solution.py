import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    L = list(range(n + 2))
    R = list(range(n + 2))
    col = list(range(n + 2))
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1
    out = []
    pos = 2

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        # a, b roots; returns new root
        if L[a] > L[b]:
            a, b = b, a
        # merge b into a (order by size not critical; use union by range size)
        parent[b] = a
        L[a] = L[a] if L[a] < L[b] else L[b]
        if R[b] > R[a]:
            R[a] = R[b]
        return a

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
            lo = L[r]
            hi = R[r]
            size = hi - lo + 1
            cnt[old] -= size
            cnt[c] += size
            col[r] = c
            if lo > 1:
                rl = find(lo - 1)
                if col[rl] == c:
                    r = union(rl, r)
            if hi < n:
                rr = find(hi + 1)
                if col[rr] == c:
                    r = union(r, rr)
            col[r] = c
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
