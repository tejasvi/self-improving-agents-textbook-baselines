import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))   # run left bound (valid at root)
    hi = list(range(n + 2))   # run right bound (valid at root)
    color = list(range(n + 2))  # run color (valid at root)
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        # a, b roots; merge into one with combined bounds
        if lo[a] > lo[b]:
            a, b = b, a
        # keep a as root (arbitrary, union by size could be added)
        parent[b] = a
        lo[a] = min(lo[a], lo[b])
        hi[a] = max(hi[a], hi[b])
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
            old = color[r]
            if old == c:
                continue
            length = hi[r] - lo[r] + 1
            cnt[old] -= length
            cnt[c] += length
            color[r] = c
            l = lo[r]
            rr = hi[r]
            if l > 1:
                lr = find(l - 1)
                if color[lr] == c:
                    r = union(lr, r)
            if rr < n:
                rr_root = find(rr + 1)
                if color[rr_root] == c:
                    r = union(r, rr_root)
            color[find(x)] = c
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
