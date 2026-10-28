"""Solution for Sum of Max Matching problem.

We are given an undirected connected weighted graph. For any two vertices x, y,
let f(x, y) be the minimum possible maximum edge weight on a path from x to y.
It is well‑known that f(x, y) equals the maximum edge weight on the unique path
between x and y in a *minimum spanning tree* (MST) of the graph.  Moreover, when we
build the so‑called Kruskal reconstruction tree, the weight of the lowest common
ancestor (LCA) of two vertices is exactly f(x, y).

We have two sequences A_1..A_K and B_1..B_K (A_i never appears in B).  We may
permute the B sequence arbitrarily.  We need the minimum possible sum of
f(A_i, B_{perm(i)}).

Observation
-----------
Consider the reconstruction tree.  Every leaf corresponds to a graph vertex.
Suppose a leaf v appears a_v times in the A‑list and b_v times in the B‑list.
When we walk the tree from leaves to the root we can greedily match as many A’s
with B’s as possible inside each subtree: any pair whose LCA lies lower in the
tree yields a smaller contribution because the LCA weight is smaller.  Therefore,
for each internal node we match `min(total_A, total_B)` pairs inside this subtree
and pass the leftover unpaired vertices upward.  The contribution of this node to
the answer is `weight[node] * matched_pairs`.

Algorithm
---------
1. Build the Kruskal reconstruction tree.
   * Sort edges by weight.
   * Maintain a DSU where each component is represented by the current root in
     the reconstruction tree.
   * For each edge (u, v, w) in increasing order, if the components are
     different, create a new node `new_id` with `weight[new_id] = w` and make the
     two component roots its children.  Union the components, with the new node
     becoming the representative.
   After processing all edges we have a single root (its id = current node count
   - 1).
2. For each vertex `i` (1‑based) count how many times it appears in A and in B.
3. Perform a post‑order traversal of the reconstruction tree (iterative stack
   because recursion depth could be ~2·10^5).  For each node we obtain the total
   numbers of A’s and B’s in its subtree, compute `matched = min(a, b)`, add
   `weight[node] * matched` to the answer and keep the surplus counts to be
   returned to the parent.
4. Output the accumulated answer.

Complexities
------------
Sorting edges: `O(M log M)`.
DSU operations: `O((N+M) α(N))`.
Tree traversal: `O(N)`.
Memory consumption: `O(N)` (the reconstruction tree has at most `2·N` nodes).

The implementation below follows this plan.
"""

import sys
sys.setrecursionlimit(1 << 25)

def solve() -> None:
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

    # ----- DSU for Kruskal reconstruction tree -----
    parent = list(range(N))  # DSU parent
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    # reconstruction tree structures
    max_nodes = 2 * N  # enough space
    weight = [0] * max_nodes  # weight of node (0 for leaves)
    children = [[] for _ in range(max_nodes)]
    cur_id = N  # next new node id

    # Sort edges by weight (ascending)
    edges.sort()
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        # create new node representing union
        nid = cur_id
        cur_id += 1
        weight[nid] = w
        children[nid].append(ru)
        children[nid].append(rv)
        # union in DSU: set both roots' representative to new node
        parent[ru] = nid
        parent[rv] = nid
        parent[nid] = nid  # new node is its own parent
    root = cur_id - 1

    # ----- count occurrences of each vertex in A and B -----
    a_cnt = [0] * cur_id
    b_cnt = [0] * cur_id
    for v in A:
        a_cnt[v] += 1
    for v in B:
        b_cnt[v] += 1

    # ----- post‑order traversal (iterative) -----
    ans = 0
    stack = [(root, 0)]  # (node, state)  state 0 = first visit, 1 = after children processed
    while stack:
        node, state = stack.pop()
        if state == 0:
            # push node again after processing children
            stack.append((node, 1))
            for ch in children[node]:
                stack.append((ch, 0))
        else:
            # aggregate from children (already computed a_cnt, b_cnt for them)
            total_a = a_cnt[node]
            total_b = b_cnt[node]
            for ch in children[node]:
                total_a += a_cnt[ch]
                total_b += b_cnt[ch]
            # match as many as possible at this node
            matched = total_a if total_a < total_b else total_b
            ans += weight[node] * matched
            # surplus to propagate upward (store back to this node)
            a_cnt[node] = total_a - matched
            b_cnt[node] = total_b - matched
    print(ans)

if __name__ == "__main__":
    solve()
