import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    p = 3
    edges = []
    for _ in range(m):
        u = int(data[p]); v = int(data[p + 1]); w = int(data[p + 2])
        p += 3
        edges.append((w, u, v))
    # signed count: +1 per A occurrence, -1 per B occurrence
    s = [0] * (n + 1)
    for i in range(k):
        s[int(data[p + i])] += 1
    p += k
    for i in range(k):
        s[int(data[p + i])] -= 1
    parent = list(range(n + 1))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    edges.sort()
    total = 0
    for w, u, v in edges:
        a = find(u)
        b = find(v)
        if a == b:
            continue
        sa = s[a]
        sb = s[b]
        if (sa > 0 and sb < 0) or (sa < 0 and sb > 0):
            total += w * min(abs(sa), abs(sb))
        parent[a] = b
        s[b] = sa + sb
    print(total)


main()
