# Solution for Sum of Max Matching problem
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        w = int(next(it))
        edges.append((w, u, v))
    A = [int(next(it)) - 1 for _ in range(K)]
    B = [int(next(it)) - 1 for _ in range(K)]

    cntA = [0] * N
    cntB = [0] * N
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    parent = list(range(N))
    size = [1] * N
    a = cntA[:]  # remaining A count in component
    b = cntB[:]  # remaining B count in component

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ans = 0
    edges.sort()  # increasing weight
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        # union by size (optional)
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        # match A in ru with B in rv, and A in rv with B in ru
        cross1 = min(a[ru], b[rv])
        cross2 = min(a[rv], b[ru])
        matched = cross1 + cross2
        ans += matched * w
        # update component counts after removing matched pairs
        a_new = a[ru] + a[rv] - matched
        b_new = b[ru] + b[rv] - matched
        parent[rv] = ru
        size[ru] += size[rv]
        a[ru] = a_new
        b[ru] = b_new

    print(ans)

if __name__ == "__main__":
    solve()
