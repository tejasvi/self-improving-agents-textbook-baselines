# Write your solution here. Read from stdin, write to stdout.

def solve():
    n = int(input())
    balls = []
    for _ in range(n):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    MOD = 998244353
    
    def get_removed(remaining_set, chosen_idx):
        """
        Given a set of remaining ball indices and a chosen ball index,
        return the set of balls that will be removed.
        """
        if chosen_idx not in remaining_set:
            return set()
        
        removed = set()
        x_k, y_k = balls[chosen_idx]
        
        for i in remaining_set:
            if i == chosen_idx:
                continue
            x_i, y_i = balls[i]
            # Remove if (X_i < X_k and Y_i < Y_k) or (X_i > X_k and Y_i > Y_k)
            if (x_i < x_k and y_i < y_k) or (x_i > x_k and y_i > y_k):
                removed.add(i)
        
        return removed
    
    # BFS to find all reachable sets
    initial_set = frozenset(range(n))
    visited = set()
    queue = [initial_set]
    visited.add(initial_set)
    
    while queue:
        current_set = queue.pop(0)
        
        # Try choosing each ball in the current set
        for chosen_idx in current_set:
            removed = get_removed(current_set, chosen_idx)
            next_set = frozenset(current_set - removed)
            
            if next_set not in visited:
                visited.add(next_set)
                queue.append(next_set)
    
    print(len(visited) % MOD)

solve()
