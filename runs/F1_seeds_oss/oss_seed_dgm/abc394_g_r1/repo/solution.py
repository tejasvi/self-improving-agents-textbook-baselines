# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = H * W
    F = [0] * N
    for i in range(H):
        for j in range(W):
            F[i * W + j] = int(next(it))
    Q = int(next(it))
    queries = []  # list of (start_id, target_id, Y, Z)
    for _ in range(Q):
        A = int(next(it)) - 1
        B = int(next(it)) - 1
        Y = int(next(it))
        C = int(next(it)) - 1
        D = int(next(it)) - 1
        Z = int(next(it))
        s = A * W + B
        t = C * W + D
        queries.append((s, t, Y, Z))

    # Build edges with weight = min(F_u, F_v)
    edges = []  # (weight, u, v)
    for i in range(H):
        for j in range(W):
            u = i * W + j
            if i + 1 < H:
                v = (i + 1) * W + j
                w = F[u] if F[u] < F[v] else F[v]
                edges.append((w, u, v))
            if j + 1 < W:
                v = i * W + (j + 1)
                w = F[u] if F[u] < F[v] else F[v]
                edges.append((w, u, v))
    edges.sort(key=lambda x: x[0], reverse=True)

    parent = list(range(N))
    size = [1] * N
    # queries per component
    comp_queries = [[] for _ in range(N)]  # list of (qid, other_node)
    for qid, (s, t, _, _) in enumerate(queries):
        comp_queries[s].append((qid, t))
        comp_queries[t].append((qid, s))
    # result thresholds, -1 means not yet determined
    thr = [-1] * Q

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        # union by size: ensure ru is larger
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        # merge rv into ru
        # process queries in smaller component (rv)
        for qid, other in comp_queries[rv]:
            if thr[qid] != -1:
                continue
            if find(other) == ru:
                thr[qid] = w
            else:
                comp_queries[ru].append((qid, other))
        comp_queries[rv].clear()
        parent[rv] = ru
        size[ru] += size[rv]

    # For any queries still unresolved (should not happen), set threshold to 0
    for i in range(Q):
        if thr[i] == -1:
            thr[i] = 0

    out_lines = []
    for i, (s, t, Y, Z) in enumerate(queries):
        T = thr[i]
        if T >= min(Y, Z):
            ans = abs(Y - Z)
        else:
            ans = Y + Z - 2 * T
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
