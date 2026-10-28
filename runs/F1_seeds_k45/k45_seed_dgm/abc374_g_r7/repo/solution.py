from collections import defaultdict

def solve():
    n = int(input())
    products = []
    for _ in range(n):
        products.append(input().strip())
    
    # Build graph
    # in_degree[node] = number of edges coming into node
    # out_degree[node] = number of edges going out from node
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    # Track which nodes are in the graph
    nodes = set()
    
    for product in products:
        u, v = product[0], product[1]
        out_degree[u] += 1
        in_degree[v] += 1
        nodes.add(u)
        nodes.add(v)
    
    # Check Eulerian path conditions
    # Count nodes with unbalanced degrees
    excess_out = 0  # nodes where out-degree > in-degree
    excess_in = 0   # nodes where in-degree > out-degree
    
    for node in nodes:
        diff = out_degree[node] - in_degree[node]
        if diff > 0:
            excess_out += diff
        elif diff < 0:
            excess_in += -diff
    
    # The minimum number of paths needed is max(excess_out, excess_in)
    # But since excess_out == excess_in (total in = total out in any graph),
    # we just need one of them
    
    # Actually, the formula is:
    # If excess_out == 0, we have an Eulerian circuit/path → answer is 1
    # Otherwise, we need excess_out paths (or equivalently excess_in paths)
    
    if excess_out == 0:
        return 1
    else:
        return excess_out

print(solve())
