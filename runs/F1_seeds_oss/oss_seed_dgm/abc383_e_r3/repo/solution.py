# Solution for "Sum of Max Matching"
# Author: OpenAI's ChatGPT

import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = []
    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((w, u, v))
    A = [int(next(it)) for _ in range(K)]
    B = [int(next(it)) for _ in range(K)]

    # Count occurrences of each vertex in A and B
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    parent = list(range(N + 1))
    # component aggregates
    compA = cntA[:]  # copy of counts per component (initially each vertex its own component)
    compB = cntB[:]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = 0
    # Process edges in non‑decreasing order of weight (Kruskal style)
    edges.sort(key=lambda e: e[0])
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        # New pairs that become connectable across the two components
        new_pairs = compA[ru] * compB[rv] + compA[rv] * compB[ru]
        answer += new_pairs * w
        # Union by size (optional, to keep tree shallow)
        if (compA[ru] + compB[ru]) < (compA[rv] + compB[rv]):
            ru, rv = rv, ru
        # merge rv into ru
        parent[rv] = ru
        compA[ru] += compA[rv]
        compB[ru] += compB[rv]
    print(answer)

if __name__ == "__main__":
    solve()
