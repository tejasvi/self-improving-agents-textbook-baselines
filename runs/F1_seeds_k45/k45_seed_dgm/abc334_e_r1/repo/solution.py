from collections import deque

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def read_input():
    H, W = map(int, input().split())
    grid = []
    for _ in range(H):
        grid.append(input().strip())
    return H, W, grid

def get_neighbors(i, j, H, W):
    """Get valid neighbors of cell (i, j)"""
    neighbors = []
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < H and 0 <= nj < W:
            neighbors.append((ni, nj))
    return neighbors

def count_components(grid, H, W):
    """Count the number of green connected components"""
    visited = [[False] * W for _ in range(H)]
    components = 0
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and not visited[i][j]:
                # BFS to mark all cells in this component
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    ci, cj = queue.popleft()
                    for ni, nj in get_neighbors(ci, cj, H, W):
                        if grid[ni][nj] == '#' and not visited[ni][nj]:
                            visited[ni][nj] = True
                            queue.append((ni, nj))
                components += 1
    
    return components

def get_component_id(grid, H, W):
    """Get the component ID for each green cell"""
    comp_id = [[-1] * W for _ in range(H)]
    visited = [[False] * W for _ in range(H)]
    comp_num = 0
    
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and not visited[i][j]:
                # BFS to mark all cells in this component
                queue = deque([(i, j)])
                visited[i][j] = True
                comp_id[i][j] = comp_num
                while queue:
                    ci, cj = queue.popleft()
                    for ni, nj in get_neighbors(ci, cj, H, W):
                        if grid[ni][nj] == '#' and not visited[ni][nj]:
                            visited[ni][nj] = True
                            comp_id[ni][nj] = comp_num
                            queue.append((ni, nj))
                comp_num += 1
    
    return comp_id, comp_num

def solve():
    H, W, grid = read_input()
    
    # Count initial green components
    initial_components = count_components(grid, H, W)
    
    # Get component IDs
    comp_id, comp_count = get_component_id(grid, H, W)
    
    # Collect all red cells
    red_cells = []
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_cells.append((i, j))
    
    num_red_cells = len(red_cells)
    
    total = 0
    
    # For each red cell, compute the resulting number of components
    for ri, rj in red_cells:
        # Find unique adjacent component IDs
        adjacent_comps = set()
        for ni, nj in get_neighbors(ri, rj, H, W):
            if grid[ni][nj] == '#':
                adjacent_comps.add(comp_id[ni][nj])
        
        # The new number of components is:
        # initial_components - (number of adjacent components - 1) + 1
        # = initial_components - number of adjacent components + 2
        # But if there are no adjacent green cells, we just add 1
        # So: initial_components + 1 - number of adjacent components + 1
        # = initial_components + 2 - number of adjacent components
        
        if len(adjacent_comps) == 0:
            # New isolated component
            new_components = initial_components + 1
        else:
            # Merge adjacent components into one
            new_components = initial_components - len(adjacent_comps) + 1
        
        total += new_components
    
    # Expected value = total / num_red_cells
    # We need to compute this modulo MOD
    total_mod = total % MOD
    inv = modinv(num_red_cells, MOD)
    result = (total_mod * inv) % MOD
    
    print(result)

solve()
