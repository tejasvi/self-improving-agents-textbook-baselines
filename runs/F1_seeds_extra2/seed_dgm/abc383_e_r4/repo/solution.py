import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    edges = []
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    A = [int(data[idx + i]) - 1 for i in range(k)]
    idx += k
    B = [int(data[idx + i]) - 1 for i in range(k)]

    # sa[v]/sb[v]: unmatched A / B counts in the component rooted at v
    sa = [0] * n
    sb = [0] * n
    for x in A:
        sa[x] += 1
    for x in B:
        sb[x] += 1

    parent = list(range(n))

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
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        a = sa[ru] + sa[rv]
        b = sb[ru] + sb[rv]
        mt = a if a < b else b
        total += mt * w
        parent[rv] = ru
        sa[ru] = a - mt
        sb[ru] = b - mt
    print(total)


main()
