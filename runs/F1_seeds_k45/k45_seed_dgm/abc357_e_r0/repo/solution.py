def solve():
    n = int(input())
    edges = list(map(int, input().split()))
    
    # Convert to 0-indexed: graph[i] is where vertex i points to
    graph = [x - 1 for x in edges]
    
    total_reachable = 0
    
    # For each starting vertex
    for u in range(n):
        reachable = set()
        current = u
        visited_in_path = set()
        
        # Follow edges until we hit a cycle or revisit a vertex
        while current not in visited_in_path:
            visited_in_path.add(current)
            reachable.add(current)
            current = graph[current]
        
        # Once we're in a cycle, all vertices in reachable at this point
        # are reachable from u. The while loop stops when current is 
        # in visited_in_path (i.e., we've found a cycle/revisited vertex),
        # so reachable contains all vertices from u until cycle.
        
        total_reachable += len(reachable)
    
    print(total_reachable)

solve()
