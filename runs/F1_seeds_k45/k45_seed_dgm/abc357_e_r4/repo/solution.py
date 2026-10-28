# Read input
N = int(input())
a = list(map(int, input().split()))

# Convert to 0-indexed
edges = [x - 1 for x in a]

# Count reachable pairs
count = 0

# For each starting vertex u
for u in range(N):
    visited = set()
    current = u
    
    # Follow edges from u until we revisit a vertex (entering the cycle)
    while current not in visited:
        visited.add(current)
        current = edges[current]
    
    # All vertices in visited are reachable from u
    count += len(visited)

print(count)
