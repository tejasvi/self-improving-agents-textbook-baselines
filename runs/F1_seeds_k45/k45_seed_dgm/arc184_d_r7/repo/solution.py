def solve():
    MOD = 998244353
    
    N = int(input())
    balls = []
    for i in range(N):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    def dominates(i, j):
        """Check if ball i dominates ball j"""
        xi, yi = balls[i]
        xj, yj = balls[j]
        return (xi < xj and yi < yj) or (xi > xj and yi > yj)
    
    # Use DFS with memoization to find all reachable states
    # State is represented as a frozenset of remaining ball indices
    visited = set()
    
    def dfs(state):
        if state in visited:
            return
        visited.add(state)
        
        # Try choosing each remaining ball
        for chosen_idx in state:
            # Determine which balls to remove
            to_remove = set()
            for i in state:
                if i != chosen_idx and dominates(chosen_idx, i):
                    to_remove.add(i)
            
            if to_remove:
                # Create new state with balls removed
                new_state = state - to_remove
                dfs(new_state)
    
    initial_state = frozenset(range(N))
    dfs(initial_state)
    
    print(len(visited) % MOD)

solve()
