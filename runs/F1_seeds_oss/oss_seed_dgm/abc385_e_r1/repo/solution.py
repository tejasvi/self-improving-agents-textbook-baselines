# Snowflake Tree solution
# The task: delete minimum vertices from a given tree so that the remaining tree is a "snowflake"
# (one central vertex, x intermediate vertices attached to it, each intermediate has y leaf children).
# Approach:
#   - For each vertex v compute leaf_nb[v] = number of leaf neighbours in the original tree.
#   - nonleaf_nb[v] = degree[v] - leaf_nb[v].
#   - If nonleaf_nb[v] == 1, then v has exactly one non‑leaf neighbour; we record that neighbour as the only possible
#     central vertex for which v could serve as an intermediate node.
#   - For each possible central vertex r we collect leaf_nb[v] of all neighbours v that satisfy the above condition and also
#     leaf_nb[v] > 0 (otherwise v would have no leaf children to keep).
#   - From this multiset we may choose any k ≥ 1 of them. To keep a snowflake we must keep the same number y of leaf children
#     for each selected intermediate. The maximum feasible y for a chosen set is the minimum leaf_nb among the selected vertices
#     (we can delete extra leaves). Therefore for a sorted descending list cand we consider taking the first k elements;
#     the limiting y is cand[k‑1]. The number of kept vertices is 1 + k * (1 + y).
#   - We maximise this value over all roots and k.
#   - Answer = N - max_keep.

import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)

    deg = [len(adj[i]) for i in range(n)]
    is_leaf = [d == 1 for d in deg]

    # leaf_nb[v] = number of neighbours of v that are leaves in the original tree
    leaf_nb = [0] * n
    for v in range(n):
        cnt = 0
        for nb in adj[v]:
            if is_leaf[nb]:
                cnt += 1
        leaf_nb[v] = cnt

    nonleaf_nb = [deg[i] - leaf_nb[i] for i in range(n)]

    # For each vertex v that has exactly one non‑leaf neighbour, store that neighbour.
    single_nonleaf = [-1] * n
    for v in range(n):
        if nonleaf_nb[v] == 1:
            for nb in adj[v]:
                if not is_leaf[nb]:
                    single_nonleaf[v] = nb
                    break

    # Build list of candidate leaf counts for each possible central vertex.
    candidates = [[] for _ in range(n)]
    for v in range(n):
        if leaf_nb[v] == 0:
            continue  # cannot be intermediate (needs leaf children)
        # v must be non‑leaf itself, otherwise leaf_nb[v] would be 0 anyway.
        if nonleaf_nb[v] == 1:
            r = single_nonleaf[v]
            # r could be -1 in degenerate case, but then nonleaf_nb[v]==1 ensures there is a non‑leaf neighbour.
            if r != -1:
                candidates[r].append(leaf_nb[v])

    max_keep = 0
    for r in range(n):
        cand = candidates[r]
        if not cand:
            continue
        cand.sort(reverse=True)
        # iterate over possible number of intermediate vertices k
        for k in range(1, len(cand) + 1):
            y = cand[k - 1]          # smallest leaf count among the chosen k
            kept = 1 + k * (1 + y)   # root + k intermediates + k*y leaves
            if kept > max_keep:
                max_keep = kept

    # Safety fallback (the problem guarantees a solution with at least 3 vertices)
    if max_keep == 0:
        max_keep = 1
    ans = n - max_keep
    print(ans)

if __name__ == "__main__":
    solve()
