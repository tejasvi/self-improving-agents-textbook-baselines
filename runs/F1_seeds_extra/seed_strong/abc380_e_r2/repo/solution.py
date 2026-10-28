import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    color = list(range(n + 2))
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        # a, b are roots; merge into one, return new root
        if lo[a] > lo[b]:
            a, b = b, a
        # keep a as root (arbitrary, use size-free union with path halving)
        parent[b] = a
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
            a = color[r]
            if a == c:
                continue
            L = lo[r]
            R = hi[r]
            cnt[a] -= R - L + 1
            cnt[c] += R - L + 1
            color[r] = c
            cur = r
            if L > 1:
                lr = find(L - 1)
                if color[lr] == c:
                    cur = union(cur, lr)
            if R < n:
                rr = find(R + 1)
                if color[rr] == c:
                    cur = union(cur, rr)
            color[cur] = c
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
