def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Convert to 0-indexed
    a = [x - 1 for x in a]
    
    total_count = 0
    
    # For each starting vertex u
    for u in range(n):
        # Find all vertices reachable from u
        visited = set()
        current = u
        
        # Follow the path until we revisit a vertex (enter a cycle)
        while current not in visited:
            visited.add(current)
            current = a[current]
        
        # At this point, current is the first vertex we revisit
        # All vertices in visited are reachable from u
        total_count += len(visited)
    
    print(total_count)

solve()
