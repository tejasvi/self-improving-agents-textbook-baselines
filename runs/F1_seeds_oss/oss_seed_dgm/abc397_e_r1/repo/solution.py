# Solution for Path Decomposition of a Tree
# Reads a tree with NK vertices and decides whether it can be split into N vertex‑disjoint
# paths each containing exactly K vertices (i.e. K‑1 edges).
# The algorithm is a classic bottom‑up DP on a rooted tree.
# For each node we receive from its children the length (in edges) of the unique
# unfinished path that is waiting to be extended upwards.  Length 0 means the
# child subtree is already completely covered.
# When a child's length becomes K‑1 after adding the edge to the parent we can
# close a whole path there and discard it.
# The remaining lengths must be paired so that the sum of the two lengths is K‑1;
# this corresponds to joining two unfinished tails at the current node to form a
# complete path.  At most one length may remain unpaired – it will be propagated
# to the parent (increased by one edge).
# If at any node we cannot achieve this, the decomposition is impossible.

import sys
sys.setrecursionlimit(1 << 25)

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    total = N * K
    # Build adjacency list (0‑based)
    g = [[] for _ in range(total)]
    for _ in range(total - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        g[u].append(v)
        g[v].append(u)

    # Trivial case: K == 1, each vertex forms a path.
    if K == 1:
        print("Yes")
        return

    def dfs(u: int, parent: int) -> int:
        """Return the length (in edges) of the single unfinished path that
        leaves the subtree rooted at u and goes towards its parent.
        Return -1 if the subtree cannot be decomposed.
        """
        lengths = []
        for v in g[u]:
            if v == parent:
                continue
            child_len = dfs(v, u)
            if child_len == -1:
                return -1
            # extend the child's unfinished path by the edge (u, v)
            child_len += 1
            if child_len == K - 1:
                # completed a whole path of K vertices, discard it
                continue
            if child_len > K - 1:
                return -1
            lengths.append(child_len)

        # Pair lengths so that each pair sums to K-1.
        # Use a two‑pointer technique on the sorted list.
        lengths.sort()
        m = len(lengths)
        used = [False] * m
        i, j = 0, m - 1
        while i < j:
            s = lengths[i] + lengths[j]
            if s == K - 1:
                used[i] = used[j] = True
                i += 1
                j -= 1
            elif s < K - 1:
                i += 1
            else:  # s > K - 1
                j -= 1
        leftovers = [lengths[idx] for idx, ok in enumerate(used) if not ok]
        if len(leftovers) > 1:
            return -1
        if leftovers:
            return leftovers[0]
        return 0

    root_res = dfs(0, -1)
    print("Yes" if root_res == 0 else "No")

if __name__ == "__main__":
    solve()
