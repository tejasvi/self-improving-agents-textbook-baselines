# Write your solution here. Read from stdin, write to stdout.

from collections import deque

N, Q = map(int, input().split())

# Initialize colors: colors[i] is the color of cell i (1-indexed)
colors = [0] + list(range(1, N + 1))  # colors[0] unused, colors[1..N]

for _ in range(Q):
    query = list(map(int, input().split()))
    
    if query[0] == 1:
        # Type 1: Repaint all reachable cells from x with the same color
        x, c = query[1], query[2]
        
        # Find all cells reachable from x with the same color as x
        original_color = colors[x]
        visited = [False] * (N + 1)
        queue = deque([x])
        visited[x] = True
        reachable = [x]
        
        while queue:
            cell = queue.popleft()
            
            # Check left neighbor
            if cell > 1 and not visited[cell - 1] and colors[cell - 1] == original_color:
                visited[cell - 1] = True
                queue.append(cell - 1)
                reachable.append(cell - 1)
            
            # Check right neighbor
            if cell < N and not visited[cell + 1] and colors[cell + 1] == original_color:
                visited[cell + 1] = True
                queue.append(cell + 1)
                reachable.append(cell + 1)
        
        # Repaint all reachable cells
        for cell in reachable:
            colors[cell] = c
    
    else:
        # Type 2: Count cells with color c
        c = query[1]
        count = sum(1 for i in range(1, N + 1) if colors[i] == c)
        print(count)
