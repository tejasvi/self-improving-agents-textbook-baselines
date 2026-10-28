import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2]); idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]) - 1; v = int(data[idx + 1]) - 1; w = int(data[idx + 2]); idx += 3
        edges.append((w, u, v))
    A = [int(x) - 1 for x in data[idx:idx + k]]; idx += k
    B = [int(x) - 1 for x in data[idx:idx + k]]; idx += k

    parent = list(range(n))
    ca = [0] * n
    cb = [0] * n
    for x in A:
        ca[x] += 1
    for x in B:
        cb[x] += 1

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    edges.sort()
    ans = 0
    for w, u, v in edges:
        r1 = find(u); r2 = find(v)
        if r1 == r2:
            continue
        m1 = min(ca[r1], cb[r2])
        ca[r1] -= m1; cb[r2] -= m1
        ans += w * m1
        m2 = min(ca[r2], cb[r1])
        ca[r2] -= m2; cb[r1] -= m2
        ans += w * m2
        # merge r2 into r1
        parent[r2] = r1
        ca[r1] += ca[r2]; cb[r1] += cb[r2]
    print(ans)

main()
