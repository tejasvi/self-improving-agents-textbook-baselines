MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def count_components(grid, H, W):
    """Count the number of green connected components using DFS"""
    visited = [[False] * W for _ in range(H)]
    components = 0
    
    def dfs(i, j):
        if i < 0 or i >= H or j < 0 or j >= W:
            return
        if visited[i][j] or grid[i][j] == '.':
            return
        visited[i][j] = True
        # Check all 4 adjacent cells
        dfs(i - 1, j)
        dfs(i + 1, j)
        dfs(i, j - 1)
        dfs(i, j + 1)
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and not visited[i][j]:
                dfs(i, j)
                components += 1
    
    return components

def solve():
    # Read input
    H, W = map(int, input().split())
    grid = []
    for _ in range(H):
        grid.append(list(input().strip()))
    
    # Find all red cells
    red_cells = []
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_cells.append((i, j))
    
    num_red = len(red_cells)
    total_components = 0
    
    # For each red cell, paint it green and count components
    for ri, rj in red_cells:
        # Create a copy of the grid with this cell painted green
        test_grid = [row[:] for row in grid]
        test_grid[ri][rj] = '#'
        
        # Count components in the modified grid
        comp_count = count_components(test_grid, H, W)
        total_components += comp_count
    
    # Calculate expected value: total_components / num_red
    # In modular arithmetic: (total_components * modinv(num_red)) % MOD
    result = (total_components * modinv(num_red)) % MOD
    print(result)

solve()
