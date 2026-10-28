from collections import deque

def solve():
    MOD = 998244353
    
    H, W = map(int, input().split())
    grid = [input().strip() for _ in range(H)]
    
    # Find all red cells
    red_cells = []
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_cells.append((i, j))
    
    # Get component ID for each green cell
    def get_component_ids(g):
        comp_id = [[-1] * W for _ in range(H)]
        comp_count = 0
        
        for i in range(H):
            for j in range(W):
                if g[i][j] == '#' and comp_id[i][j] == -1:
                    # BFS to mark all cells in this component
                    queue = deque([(i, j)])
                    comp_id[i][j] = comp_count
                    while queue:
                        x, y = queue.popleft()
                        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < H and 0 <= ny < W and comp_id[nx][ny] == -1 and g[nx][ny] == '#':
                                comp_id[nx][ny] = comp_count
                                queue.append((nx, ny))
                    comp_count += 1
        
        return comp_id, comp_count
    
    # Calculate the number of green components in original grid
    comp_id, original_components = get_component_ids(grid)
    
    # For each red cell, calculate the new component count
    total = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for ri, rj in red_cells:
        # Find adjacent green components
        adjacent_comps = set()
        for dx, dy in directions:
            ni, nj = ri + dx, rj + dy
            if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == '#':
                adjacent_comps.add(comp_id[ni][nj])
        
        # If we paint this red cell green:
        # - If it has no adjacent green cells, we add 1 new component
        # - If it has adjacent green cells from k different components, we merge them into 1
        # New count = original_components - (len(adjacent_comps) - 1)
        # = original_components - len(adjacent_comps) + 1
        
        if len(adjacent_comps) == 0:
            # Add a new isolated green component
            new_components = original_components + 1
        else:
            # Merge adjacent_comps into one, reducing count by (len(adjacent_comps) - 1)
            new_components = original_components - (len(adjacent_comps) - 1)
        
        total += new_components
    
    # Expected value = total / len(red_cells)
    # We need to compute total * modular_inverse(len(red_cells)) mod MOD
    
    num_red = len(red_cells)
    
    # Modular inverse using Fermat's little theorem: a^(-1) ≡ a^(p-2) (mod p)
    inv_num_red = pow(num_red, MOD - 2, MOD)
    
    result = (total % MOD) * inv_num_red % MOD
    print(result)

solve()
