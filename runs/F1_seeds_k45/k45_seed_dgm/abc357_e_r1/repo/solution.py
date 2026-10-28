def solve():
    n = int(input())
    edges = list(map(int, input().split()))
    
    # Convert to 0-indexed
    graph = [x - 1 for x in edges]
    
    count = 0
    
    # For each starting vertex u
    for u in range(n):
        # Find all vertices reachable from u
        visited = set()
        current = u
        
        # Follow the edges until we revisit a vertex (cycle detection)
        while current not in visited:
            visited.add(current)
            current = graph[current]
        
        # At this point, we've found all reachable vertices from u
        # because each vertex has exactly one outgoing edge
        count += len(visited)
    
    print(count)

solve()
