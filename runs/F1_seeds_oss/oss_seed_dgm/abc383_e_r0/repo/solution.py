# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    input_data = sys.stdin.read().split()
    it = iter(input_data)
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

    # Kruskal reconstruction tree
    # maximum number of nodes = 2*N
    max_nodes = 2 * N
    parent = list(range(max_nodes + 1))  # DSU parent for components
    weight = [0] * (max_nodes + 1)       # weight for internal nodes
    left_child = [0] * (max_nodes + 1)
    right_child = [0] * (max_nodes + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    current_id = N
    edges.sort()
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        current_id += 1
        weight[current_id] = w
        left_child[current_id] = ru
        right_child[current_id] = rv
        parent[ru] = current_id
        parent[rv] = current_id
        parent[current_id] = current_id

    root = find(1)
    total_nodes = current_id

    # counts of A and B in each subtree
    a_cnt = [0] * (total_nodes + 1)
    b_cnt = [0] * (total_nodes + 1)
    for v in A:
        a_cnt[v] += 1
    for v in B:
        b_cnt[v] += 1

    # Process nodes in increasing order (children have smaller indices)
    cost = 0
    for node in range(N + 1, total_nodes + 1):
        l = left_child[node]
        r = right_child[node]
        a_cnt[node] = a_cnt[l] + a_cnt[r]
        b_cnt[node] = b_cnt[l] + b_cnt[r]
        pairs_child = min(a_cnt[l], b_cnt[l]) + min(a_cnt[r], b_cnt[r])
        pairs_node = min(a_cnt[node], b_cnt[node])
        new_pairs = pairs_node - pairs_child
        if new_pairs:
            cost += weight[node] * new_pairs

    print(cost)

if __name__ == "__main__":
    solve()
