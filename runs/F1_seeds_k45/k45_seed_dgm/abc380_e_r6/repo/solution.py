# Write your solution here. Read from stdin, write to stdout.

from collections import deque

def solve():
    N, Q = map(int, input().split())
    
    # Initialize colors: cell i has color i (1-indexed)
    colors = [0] + list(range(1, N + 1))  # index 0 unused, indices 1 to N
    
    for _ in range(Q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # Type 1: Recolor connected component
            x, c = query[1], query[2]
            
            # BFS to find all connected cells with the same color as cell x
            original_color = colors[x]
            visited = [False] * (N + 1)
            queue = deque([x])
            visited[x] = True
            connected_cells = [x]
            
            while queue:
                cell = queue.popleft()
                
                # Check left neighbor
                if cell > 1 and not visited[cell - 1] and colors[cell - 1] == original_color:
                    visited[cell - 1] = True
                    queue.append(cell - 1)
                    connected_cells.append(cell - 1)
                
                # Check right neighbor
                if cell < N and not visited[cell + 1] and colors[cell + 1] == original_color:
                    visited[cell + 1] = True
                    queue.append(cell + 1)
                    connected_cells.append(cell + 1)
            
            # Recolor all connected cells
            for cell in connected_cells:
                colors[cell] = c
        
        else:  # query[0] == 2
            # Type 2: Count cells with color c
            c = query[1]
            count = sum(1 for i in range(1, N + 1) if colors[i] == c)
            print(count)

solve()
