from collections import defaultdict, deque

def solve():
    n = int(input())
    products = []
    for _ in range(n):
        products.append(input().strip())
    
    if n == 0:
        print(0)
        return
    
    # Build a directed graph where nodes are letters
    # and edges are the product names
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for product in products:
        a, b = product[0], product[1]
        graph[a].append(b)
        out_degree[a] += 1
        in_degree[b] += 1
    
    # Get all nodes that are part of products
    nodes = set()
    for product in products:
        nodes.add(product[0])
        nodes.add(product[1])
    
    # The minimum number of paths needed to cover all edges equals:
    # number of nodes with out_degree > in_degree
    # (these are the starting points of paths we must create)
    
    paths_needed = 0
    for node in nodes:
        if out_degree[node] > in_degree[node]:
            paths_needed += out_degree[node] - in_degree[node]
    
    # If all nodes have in_degree == out_degree, we have cycles
    # and need at least 1 path
    if paths_needed == 0:
        paths_needed = 1
    
    print(paths_needed)

solve()
