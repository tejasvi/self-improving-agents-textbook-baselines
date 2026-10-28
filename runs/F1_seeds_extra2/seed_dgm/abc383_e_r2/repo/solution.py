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
    a_cnt = [0] * n
    b_cnt = [0] * n
    for _ in range(k):
        a_cnt[int(data[idx]) - 1] += 1
        idx += 1
    for _ in range(k):
        b_cnt[int(data[idx]) - 1] += 1
        idx += 1

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
        a = a_cnt[ru] + a_cnt[rv]
        b = b_cnt[ru] + b_cnt[rv]
        matched = a if a < b else b
        total += matched * w
        parent[rv] = ru
        a_cnt[ru] = a - matched
        b_cnt[ru] = b - matched
        a_cnt[rv] = 0
        b_cnt[rv] = 0
    print(total)


main()
