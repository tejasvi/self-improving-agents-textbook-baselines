def solve():
    n = int(input())
    edges = list(map(int, input().split()))
    
    # Convert to 0-indexed
    graph = [edges[i] - 1 for i in range(n)]
    
    count = 0
    
    # For each starting vertex u
    for u in range(n):
        # Find all vertices reachable from u
        visited = set()
        current = u
        
        # Keep following edges until we revisit a vertex
        while current not in visited:
            visited.add(current)
            current = graph[current]
        
        # All vertices in visited are reachable from u
        count += len(visited)
    
    print(count)

solve()
