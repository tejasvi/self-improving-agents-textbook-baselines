def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Convert to 0-indexed
    edges = [x - 1 for x in a]
    
    total_count = 0
    
    # For each starting vertex u
    for u in range(n):
        # Find all vertices reachable from u
        visited = set()
        current = u
        
        # Follow the edges from u until we revisit a vertex
        while current not in visited:
            visited.add(current)
            current = edges[current]
        
        # Count the reachable vertices
        total_count += len(visited)
    
    print(total_count)

solve()
