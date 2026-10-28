from collections import defaultdict

def solve():
    n = int(input())
    
    if n < 3:
        print(0)
        return
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    max_kept = 0
    
    # Try each vertex as the root of the snowflake tree
    for root in range(1, n + 1):
        # Get neighbors of root (potential intermediate vertices)
        neighbors = adj[root]
        
        if len(neighbors) == 0:
            continue
        
        # For each neighbor, count how many leaves it has
        # (neighbors excluding the root)
        leaf_counts = []
        for neighbor in neighbors:
            leaf_count = len(adj[neighbor]) - 1  # -1 to exclude root
            if leaf_count > 0:
                leaf_counts.append(leaf_count)
        
        if not leaf_counts:
            continue
        
        # Sort leaf counts in descending order
        leaf_counts.sort(reverse=True)
        
        # Try each possible y value from 1 to max leaf count
        max_y = leaf_counts[0]
        
        for y in range(1, max_y + 1):
            # Count how many children have at least y leaves
            x = 0
            for count in leaf_counts:
                if count >= y:
                    x += 1
                else:
                    break  # Since sorted in descending order
            
            if x == 0:
                break
            
            # Calculate total vertices in this snowflake tree
            # 1 (root) + x (children) + x*y (leaves)
            kept = 1 + x + x * y
            max_kept = max(max_kept, kept)
    
    print(n - max_kept)

solve()
