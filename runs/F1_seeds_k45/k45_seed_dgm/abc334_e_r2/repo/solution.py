MOD = 998244353

def modinv(a, mod=MOD):
    """Calculate modular inverse using Fermat's little theorem"""
    return pow(a, mod - 2, mod)

def count_connected_components(grid, h, w):
    """Count the number of green connected components using BFS"""
    visited = [[False] * w for _ in range(h)]
    count = 0
    
    def bfs(si, sj):
        from collections import deque
        queue = deque([(si, sj)])
        visited[si][sj] = True
        while queue:
            i, j = queue.popleft()
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and grid[ni][nj] == '#':
                    visited[ni][nj] = True
                    queue.append((ni, nj))
    
    for i in range(h):
        for j in range(w):
            if grid[i][j] == '#' and not visited[i][j]:
                bfs(i, j)
                count += 1
    
    return count

def solve():
    # Read input
    h, w = map(int, input().split())
    grid = []
    for _ in range(h):
        grid.append(list(input().strip()))
    
    # Find all red cells
    red_cells = []
    for i in range(h):
        for j in range(w):
            if grid[i][j] == '.':
                red_cells.append((i, j))
    
    num_red = len(red_cells)
    
    # For each red cell, calculate the number of connected components after painting it green
    total_components = 0
    
    for ri, rj in red_cells:
        # Paint the cell green
        grid[ri][rj] = '#'
        
        # Count connected components
        components = count_connected_components(grid, h, w)
        total_components += components
        
        # Restore the cell to red
        grid[ri][rj] = '.'
    
    # Calculate expected value: total_components / num_red (mod MOD)
    # This is (total_components * modinv(num_red)) mod MOD
    result = (total_components * modinv(num_red)) % MOD
    print(result)

solve()
