# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict

def solve():
    n = int(input())
    used_products = set()
    graph = defaultdict(list)  # graph[u] = list of v where u->v is a used product
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    all_nodes = set()
    
    for _ in range(n):
        product = input().strip()
        used_products.add(product)
        u, v = product[0], product[1]
        graph[u].append(v)
        out_degree[u] += 1
        in_degree[v] += 1
        all_nodes.add(u)
        all_nodes.add(v)
    
    # The minimum number of paths needed to cover all edges in a directed graph
    # can be computed using the formula:
    # min_paths = sum of max(0, in_degree[v] - out_degree[v]) for all v
    # This counts the imbalance - nodes that have more incoming than outgoing edges
    # Each such node requires a path to end at it
    
    min_paths = 0
    for node in all_nodes:
        imbalance = in_degree[node] - out_degree[node]
        if imbalance > 0:
            min_paths += imbalance
    
    # If min_paths is 0, we have an Eulerian circuit/path, need 1 path
    if min_paths == 0:
        min_paths = 1
    
    print(min_paths)

solve()
