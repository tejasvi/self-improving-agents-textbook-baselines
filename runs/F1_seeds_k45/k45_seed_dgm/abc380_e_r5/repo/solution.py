# Write your solution here. Read from stdin, write to stdout.

from collections import deque

def main():
    N, Q = map(int, input().split())
    
    # Initialize colors: cell i (1-indexed) has color i
    colors = [0] + list(range(1, N + 1))  # index 0 unused, colors[i] is color of cell i
    
    for _ in range(Q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # Type 1: recolor all cells reachable from cell x to color c
            x, c = query[1], query[2]
            
            # BFS to find all cells with the same color as cell x
            old_color = colors[x]
            if old_color == c:
                continue  # No need to recolor if already the same color
            
            # BFS to find all connected cells with old_color
            visited = set()
            queue = deque([x])
            visited.add(x)
            
            while queue:
                cell = queue.popleft()
                colors[cell] = c
                
                # Check adjacent cells
                if cell > 1 and colors[cell - 1] == old_color and cell - 1 not in visited:
                    visited.add(cell - 1)
                    queue.append(cell - 1)
                if cell < N and colors[cell + 1] == old_color and cell + 1 not in visited:
                    visited.add(cell + 1)
                    queue.append(cell + 1)
        
        else:
            # Type 2: count cells with color c
            c = query[1]
            count = sum(1 for i in range(1, N + 1) if colors[i] == c)
            print(count)

if __name__ == "__main__":
    main()
