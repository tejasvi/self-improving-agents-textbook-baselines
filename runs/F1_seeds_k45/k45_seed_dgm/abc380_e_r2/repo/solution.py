from collections import deque, defaultdict

def main():
    N, Q = map(int, input().split())
    
    # Initialize colors: colors[i] is the color of cell i+1
    colors = list(range(1, N + 1))
    
    # Maintain count of each color
    color_count = defaultdict(int)
    for i in range(N):
        color_count[colors[i]] += 1
    
    for _ in range(Q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # Type 1: Recolor query
            x = query[1] - 1  # Convert to 0-indexed
            c = query[2]
            
            original_color = colors[x]
            
            # If already the target color, no need to do anything
            if original_color == c:
                continue
            
            # BFS to find all connected cells with the same color
            visited = [False] * N
            queue = deque([x])
            visited[x] = True
            to_recolor = [x]
            
            while queue:
                cell = queue.popleft()
                
                # Check left neighbor
                if cell > 0 and not visited[cell - 1] and colors[cell - 1] == original_color:
                    visited[cell - 1] = True
                    queue.append(cell - 1)
                    to_recolor.append(cell - 1)
                
                # Check right neighbor
                if cell < N - 1 and not visited[cell + 1] and colors[cell + 1] == original_color:
                    visited[cell + 1] = True
                    queue.append(cell + 1)
                    to_recolor.append(cell + 1)
            
            # Recolor all found cells
            num_cells = len(to_recolor)
            for cell in to_recolor:
                colors[cell] = c
            
            # Update color counts
            color_count[original_color] -= num_cells
            color_count[c] += num_cells
        
        else:
            # Type 2: Count query
            c = query[1]
            print(color_count[c])

if __name__ == "__main__":
    main()
