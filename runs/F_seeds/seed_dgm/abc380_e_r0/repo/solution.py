import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    size = [1] * (n + 2)
    color = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b, c):
        a = find(a)
        b = find(b)
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        if lo[b] < lo[a]:
            lo[a] = lo[b]
        if hi[b] > hi[a]:
            hi[a] = hi[b]
        color[a] = c
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
            col = color[r]
            if col == c:
                continue
            l0 = lo[r]
            r0 = hi[r]
            ln = r0 - l0 + 1
            cnt[col] -= ln
            cnt[c] += ln
            color[r] = c
            if l0 > 1:
                p = find(l0 - 1)
                if color[p] == c:
                    r = union(r, p, c)
            if r0 < n:
                s = find(r0 + 1)
                if color[s] == c:
                    r = union(r, s, c)
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
