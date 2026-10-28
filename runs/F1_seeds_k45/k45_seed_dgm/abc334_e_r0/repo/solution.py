from collections import deque

MOD = 998244353

def count_green_components(grid, H, W):
    """Count the number of green connected components using BFS"""
    visited = [[False] * W for _ in range(H)]
    components = 0
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and not visited[i][j]:
                components += 1
                # BFS to mark all cells in this component
                queue = deque([(i, j)])
                visited[i][j] = True
                
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny] and grid[nx][ny] == '#':
                            visited[nx][ny] = True
                            queue.append((nx, ny))
    
    return components

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def main():
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
    
    num_red_cells = len(red_cells)
    total_components = 0
    
    # For each red cell, paint it green and count components
    for i, j in red_cells:
        # Create a copy of the grid with this cell painted green
        grid_copy = [row[:] for row in grid]
        grid_copy[i][j] = '#'
        
        # Count components
        components = count_green_components(grid_copy, H, W)
        total_components += components
    
    # Calculate expected value as P/Q
    # Expected = total_components / num_red_cells
    # We need to compute (total_components * modinv(num_red_cells)) % MOD
    
    result = (total_components * modinv(num_red_cells)) % MOD
    print(result)

if __name__ == "__main__":
    main()
