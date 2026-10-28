from collections import defaultdict

def solve():
    N = int(input())
    
    if N < 3:
        print(0)
        return
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(N - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    max_kept = 0
    
    # Try each vertex as the root
    for root in range(1, N + 1):
        neighbors = adj[root]
        num_neighbors = len(neighbors)
        
        if num_neighbors == 0:
            continue
        
        # For this root, calculate the number of leaf children for each neighbor
        leaf_counts = []
        for neighbor in neighbors:
            leaf_count = 0
            for child in adj[neighbor]:
                if child != root and len(adj[child]) == 1:
                    leaf_count += 1
            leaf_counts.append((leaf_count, neighbor))
        
        # Sort by leaf count in descending order
        leaf_counts.sort(reverse=True)
        
        # Try each possible x (number of intermediate vertices)
        for x in range(1, num_neighbors + 1):
            # Select the top x neighbors with most leaves
            selected = leaf_counts[:x]
            
            # y is the minimum number of leaves among selected intermediate vertices
            y = min(count for count, _ in selected)
            
            if y > 0:
                kept = 1 + x + x * y
                max_kept = max(max_kept, kept)
    
    print(N - max_kept)

solve()
