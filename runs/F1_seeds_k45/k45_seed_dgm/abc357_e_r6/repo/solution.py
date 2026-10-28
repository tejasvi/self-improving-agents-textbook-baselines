# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Convert to 0-indexed
    edges = [x - 1 for x in a]
    
    total_count = 0
    
    # For each starting vertex
    for u in range(n):
        visited = set()
        current = u
        
        # Keep following edges until we revisit a node
        while current not in visited:
            visited.add(current)
            current = edges[current]
        
        # All visited nodes are reachable from u
        total_count += len(visited)
    
    print(total_count)

solve()
