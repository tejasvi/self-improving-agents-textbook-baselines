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
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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

def get_component_id(grid, H, W):
    """Assign component IDs to each green cell"""
    component = [[-1] * W for _ in range(H)]
    comp_id = 0
    
    def bfs(start_i, start_j, comp_id):
        queue = deque([(start_i, start_j)])
        component[start_i][start_j] = comp_id
        
        while queue:
            i, j = queue.popleft()
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W and component[ni][nj] == -1 and grid[ni][nj] == '#':
                    component[ni][nj] = comp_id
                    queue.append((ni, nj))
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and component[i][j] == -1:
                bfs(i, j, comp_id)
                comp_id += 1
    
    return component, comp_id

def solve():
    H, W = map(int, input().split())
    grid = []
    for _ in range(H):
        grid.append(list(input().strip()))
    
    # Count initial components and get component IDs
    initial_components = count_components(grid, H, W)
    component, num_components = get_component_id(grid, H, W)
    
    # Count red cells and calculate sum
    red_cells = []
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_cells.append((i, j))
    
    num_red = len(red_cells)
    
    if num_red == 0:
        print(initial_components % MOD)
        return
    
    total = 0
    
    # For each red cell
    for i, j in red_cells:
        # Find all distinct adjacent green components
        adjacent_components = set()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == '#':
                adjacent_components.add(component[ni][nj])
        
        # Calculate the number of components after repainting
        num_adjacent = len(adjacent_components)
        
        if num_adjacent == 0:
            # The red cell becomes its own component
            new_components = initial_components + 1
        else:
            # Adjacent components merge through this cell
            # new_components = initial_components - num_adjacent + 1
            new_components = initial_components - num_adjacent + 1
        
        total = (total + new_components) % MOD
    
    # Expected value = total / num_red
    result = (total * modinv(num_red)) % MOD
    print(result)

solve()
