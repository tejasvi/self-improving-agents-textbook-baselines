# Write your solution here. Read from stdin, write to stdout.

import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input = sys.stdin.readline
    H_W = input().split()
    if not H_W:
        return
    H, W = map(int, H_W)
    H = int(H)
    W = int(W)
    N = H * W
    F = []
    for _ in range(H):
        F.extend(map(int, input().split()))
    Q = int(input())
    queries = []  # each: (src_idx, dst_idx, Y, Z)
    queries_by_node = [[] for _ in range(N)]
    for qi in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        A -= 1
        B -= 1
        C -= 1
        D -= 1
        src = A * W + B
        dst = C * W + D
        queries.append((src, dst, Y, Z))
        queries_by_node[src].append(qi)
        queries_by_node[dst].append(qi)
    # DSU structures
    parent = list(range(N))
    size = [1] * N
    active = [False] * N
    # For each component, a set of pending query ids that have exactly one endpoint in this component
    comp_queries = [set() for _ in range(N)]
    # answer for connectivity threshold L (max floor level where src and dst are connected)
    L_ans = [0] * Q  # will be filled
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y, h):
        xr = find(x)
        yr = find(y)
        if xr == yr:
            return
        # ensure xr is larger
        if size[xr] < size[yr]:
            xr, yr = yr, xr
        # merge yr into xr
        parent[yr] = xr
        size[xr] += size[yr]
        # merge query sets
        set_big = comp_queries[xr]
        set_small = comp_queries[yr]
        for q in set_small:
            if q in set_big:
                # both endpoints now in same component
                if L_ans[q] == 0:  # not set yet
                    L_ans[q] = h
                set_big.remove(q)
            else:
                set_big.add(q)
        comp_queries[yr] = set()  # clear
    # Prepare cells sorted by height descending
    cells = [(F[i], i) for i in range(N)]
    cells.sort(reverse=True)
    # Directions
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    # Process cells
    for h, idx in cells:
        active[idx] = True
        # initialize its query set with queries that involve this node
        comp_queries[idx] = set(queries_by_node[idx])
        r = idx // W
        c = idx % W
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < H and 0 <= nc < W:
                nidx = nr * W + nc
                if active[nidx]:
                    union(idx, nidx, h)
    # After processing, some queries might still have L_ans = 0 (possible when src==dst? but then they are same node, connected at its height)
    # Handle those: they are within same building, answer is its height
    for i, (src, dst, Y, Z) in enumerate(queries):
        if L_ans[i] == 0:
            # they must be the same cell (since otherwise they would have become connected at min of their heights)
            L_ans[i] = F[src]
    # Compute final answers
    out = []
    for i, (src, dst, Y, Z) in enumerate(queries):
        L = L_ans[i]
        if L >= min(Y, Z):
            out.append(str(abs(Y - Z)))
        else:
            out.append(str(Y + Z - 2 * L))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
