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

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        # a, b are distinct roots of same color
        if R[a] - L[a] < R[b] - L[b]:
            a, b = b, a
        parent[b] = a
        if L[b] < L[a]:
            L[a] = L[b]
        if R[b] > R[a]:
            R[a] = R[b]
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
            s = R[r] - L[r] + 1
            cnt[old] -= s
            cnt[c] += s
            col[r] = c
            l = L[r]
            rr = R[r]
            if l > 1:
                a = find(l - 1)
                if col[a] == c:
                    r = union(a, r)
            if rr < n:
                b = find(rr + 1)
                if col[b] == c:
                    r = union(r, b)
            col[r] = c
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
