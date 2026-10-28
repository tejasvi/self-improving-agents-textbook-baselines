import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2])
    idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    cnt = [0] * n
    for _ in range(k):
        a = int(data[idx]) - 1
        idx += 1
        cnt[a] += 1
    for _ in range(k):
        b = int(data[idx]) - 1
        idx += 1
        cnt[b] -= 1
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges.sort()
    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        s1 = cnt[ru]
        s2 = cnt[rv]
        if (s1 > 0 and s2 < 0) or (s1 < 0 and s2 > 0):
            ans += min(abs(s1), abs(s2)) * w
        parent[ru] = rv
        cnt[rv] = s1 + s2
    print(ans)


main()
