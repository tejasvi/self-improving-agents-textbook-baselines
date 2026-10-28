# Write your solution here. Read from stdin, write to stdout.

def count_reachable(n, edges):
    """
    Count the number of pairs (u, v) where v is reachable from u.
    
    Args:
        n: number of vertices
        edges: list where edges[i-1] is the destination of edge from vertex i
    
    Returns:
        total count of reachable pairs
    """
    count = 0
    
    # For each starting vertex u
    for u in range(1, n + 1):
        # Find all vertices reachable from u
        reachable = set()
        visited_in_path = set()
        current = u
        
        # Follow edges until we detect a cycle
        while current not in visited_in_path and current not in reachable:
            visited_in_path.add(current)
            reachable.add(current)
            current = edges[current - 1]  # edges is 0-indexed, vertices are 1-indexed
        
        # If we haven't found a cycle yet, continue from where we left off
        # If current is in reachable, we're in a cycle we've already explored
        if current not in reachable:
            # We found a new cycle, follow it
            cycle_start = current
            visited_in_path.add(current)
            reachable.add(current)
            current = edges[current - 1]
            while current != cycle_start:
                visited_in_path.add(current)
                reachable.add(current)
                current = edges[current - 1]
        
        # Count reachable vertices
        count += len(reachable)
    
    return count


# Read input
n = int(input())
a = list(map(int, input().split()))

# Count and print result
print(count_reachable(n, a))
