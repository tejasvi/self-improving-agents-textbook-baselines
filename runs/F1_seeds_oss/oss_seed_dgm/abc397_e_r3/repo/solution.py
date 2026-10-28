# Path Decomposition of a Tree
# Determine whether a given tree with N*K vertices can be partitioned into N vertex-disjoint paths each of length K.

import sys
sys.setrecursionlimit(1 << 25)

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    total = N * K
    adj = [[] for _ in range(total + 1)]
    for _ in range(total - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # Trivial case: each path length is 1, always possible.
    if K == 1:
        print("Yes")
        return

    # Depth‑first search returning the length of a single unfinished path that reaches the current vertex.
    # Return values:
    #   -1  : impossible configuration in the subtree.
    #    0  : no unfinished path propagates to the parent.
    #   >0  : length of the unfinished path (number of vertices) that ends at this vertex and will be extended upward.
    def dfs(v: int, parent: int) -> int:
        # freq[l] = how many child subtrees provide an unfinished path of length l (1 <= l < K)
        freq: dict[int, int] = {}
        for to in adj[v]:
            if to == parent:
                continue
            child_res = dfs(to, v)
            if child_res == -1:
                return -1
            if child_res == 0:
                continue  # child already finished a whole path
            cur_len = child_res + 1  # extend the unfinished path by edge v‑to
            if cur_len == K:
                # this forms a complete path of length K, consumes the child path completely.
                continue
            # otherwise it becomes a pending path of length cur_len (1 <= cur_len < K)
            freq[cur_len] = freq.get(cur_len, 0) + 1

        # Pair pending paths so that their lengths sum to K.
        # After pairing, at most one path may remain (which will be forwarded to the parent).
        # We use a deterministic method that works for all multisets.
        for l in list(freq.keys()):
            if l not in freq:
                continue
            need = K - l
            if need not in freq:
                continue
            if l == need:
                # pair within the same length; keep 0 or 1 leftovers depending on parity
                leftover = freq[l] % 2
                freq[l] = leftover
            else:
                pairs = min(freq[l], freq[need])
                if pairs:
                    freq[l] -= pairs
                    freq[need] -= pairs
        # Collect whatever is left.
        leftovers = []
        for length, cnt in freq.items():
            leftovers.extend([length] * cnt)
        if len(leftovers) > 1:
            return -1  # cannot merge more than one unfinished path at a vertex
        if leftovers:
            return leftovers[0]
        return 0

    # Run DFS from an arbitrary root (1). The whole tree must not leave any unfinished path.
    root_res = dfs(1, 0)
    if root_res == 0:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
