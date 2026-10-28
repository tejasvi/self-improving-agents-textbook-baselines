def solve():
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1  # Convert to 0-indexed
    Q -= 1
    
    grid = []
    for _ in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # Use DFS with memoization
    # State: frozenset of positions occupied by Takahashi
    memo = {}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    def dfs(takahashi_pos):
        # takahashi_pos is a frozenset of (i, j) positions
        state_key = takahashi_pos
        if state_key in memo:
            return memo[state_key]
        
        # Calculate current strength
        current_strength = sum(grid[i][j] for i, j in takahashi_pos)
        
        # Find all adjacent slimes that can be absorbed
        adjacent_slimes = set()
        for pi, pj in takahashi_pos:
            for di, dj in directions:
                ni, nj = pi + di, pj + dj
                if 0 <= ni < H and 0 <= nj < W:
                    if (ni, nj) not in takahashi_pos:
                        adjacent_slimes.add((ni, nj))
        
        # Try absorbing each adjacent slime that satisfies the condition
        max_strength = current_strength
        for si, sj in adjacent_slimes:
            slime_strength = grid[si][sj]
            if slime_strength < current_strength / X:
                # Can absorb this slime
                new_pos = frozenset(takahashi_pos | {(si, sj)})
                result = dfs(new_pos)
                max_strength = max(max_strength, result)
        
        memo[state_key] = max_strength
        return max_strength
    
    initial_pos = frozenset([(P, Q)])
    result = dfs(initial_pos)
    print(result)

solve()
