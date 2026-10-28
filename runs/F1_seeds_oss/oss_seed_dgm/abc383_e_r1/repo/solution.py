# Write your solution here. Read from stdin, write to stdout.
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
        u = int(next(it)); v = int(next(it)); w = int(next(it))
        edges.append((w, u, v))
    A = [int(next(it)) for _ in range(K)]
    B = [int(next(it)) for _ in range(K)]

    # Count occurrences (duplicates allowed)
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    for a in A:
        cntA[a] += 1
    for b in B:
        cntB[b] += 1

    # Kruskal reconstruction tree construction
    max_nodes = 2 * N  # maximum possible node index
    left_child = [0] * (max_nodes + 1)
    right_child = [0] * (max_nodes + 1)
    weight = [0] * (max_nodes + 1)

    parent = list(range(max_nodes + 1))  # DSU parent
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    cur_id = N
    edges.sort()  # increasing weight
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        cur_id += 1
        weight[cur_id] = w
        left_child[cur_id] = ru
        right_child[cur_id] = rv
        parent[ru] = cur_id
        parent[rv] = cur_id
        parent[cur_id] = cur_id

    root = find(1)

    # Arrays to store remaining unmatched counts in each subtree
    a_cnt = [0] * (cur_id + 1)
    b_cnt = [0] * (cur_id + 1)
    ans = 0

    # Post-order traversal without recursion
    stack = [(root, 0)]  # (node, state) state 0 = first visit, 1 = after children
    while stack:
        node, state = stack.pop()
        if node <= N:
            # leaf: original vertex
            a_cnt[node] = cntA[node]
            b_cnt[node] = cntB[node]
            continue
        if state == 0:
            # Process children first
            stack.append((node, 1))
            rc = right_child[node]
            lc = left_child[node]
            stack.append((rc, 0))
            stack.append((lc, 0))
        else:
            lc = left_child[node]
            rc = right_child[node]
            aL, bL = a_cnt[lc], b_cnt[lc]
            aR, bR = a_cnt[rc], b_cnt[rc]
            # Pairs that can be matched at this node (their LCA is this node)
            matches = min(aL, bR) + min(aR, bL)
            ans += weight[node] * matches
            # Remaining unmatched counts propagate upward
            a_cnt[node] = aL + aR - matches
            b_cnt[node] = bL + bR - matches

    print(ans)

if __name__ == "__main__":
    solve()
