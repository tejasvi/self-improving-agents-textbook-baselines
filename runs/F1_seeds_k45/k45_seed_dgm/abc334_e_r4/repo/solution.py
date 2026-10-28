from collections import deque

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def count_components(grid, H, W):
    """Count the number of green connected components"""
    visited = [[False] * W for _ in range(H)]
    components = 0
    
    def bfs(start_i, start_j):
        queue = deque([(start_i, start_j)])
        visited[start_i][start_j] = True
        while queue:
            i, j = queue.popleft()
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj] and grid[ni][nj] == '#':
                    visited[ni][nj] = True
                    queue.append((ni, nj))
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and not visited[i][j]:
                bfs(i, j)
                components += 1
    
    return components

def get_component_id(grid, H, W, i, j):
    """Get which component a green cell belongs to"""
    visited = [[False] * W for _ in range(H)]
    component_id = [[-1] * W for _ in range(H)]
    comp_num = 0
    
    def bfs(start_i, start_j, comp_id_val):
        queue = deque([(start_i, start_j)])
        visited[start_i][start_j] = True
        component_id[start_i][start_j] = comp_id_val
        while queue:
            x, y = queue.popleft()
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny] and grid[nx][ny] == '#':
                    visited[nx][ny] = True
                    component_id[nx][ny] = comp_id_val
                    queue.append((nx, ny))
    
    for x in range(H):
        for y in range(W):
            if grid[x][y] == '#' and not visited[x][y]:
                bfs(x, y, comp_num)
                comp_num += 1
    
    return component_id

def solve():
    H, W = map(int, input().split())
    grid = []
    for _ in range(H):
        grid.append(list(input().strip()))
    
    # Count initial green components
    initial_components = count_components(grid, H, W)
    
    # Get component IDs for each cell
    component_id = get_component_id(grid, H, W, 0, 0)
    
    # For each red cell, calculate the resulting number of components
    total = 0
    red_count = 0
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_count += 1
                
                # Find adjacent green components
                adjacent_components = set()
                for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == '#':
                        adjacent_components.add(component_id[ni][nj])
                
                k = len(adjacent_components)
                
                # Calculate new component count
                # When we add this red cell:
                # - If it connects k components, those k components merge into 1
                # - So: new_count = initial_components - k + 1
                new_components = initial_components - k + 1
                
                total += new_components
    
    # Calculate expected value: total / red_count
    # Result = (total * modinv(red_count)) % MOD
    result = (total % MOD) * modinv(red_count) % MOD
    print(result)

solve()
