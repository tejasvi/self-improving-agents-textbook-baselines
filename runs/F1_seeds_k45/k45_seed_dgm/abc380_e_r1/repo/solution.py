# Write your solution here. Read from stdin, write to stdout.

def main():
    N, Q = map(int, input().split())
    
    # colors[i] stores the color of cell i (0-indexed, so colors[0] is color of cell 1)
    colors = list(range(1, N + 1))
    
    for _ in range(Q):
        query = list(map(int, input().split()))
        
        if query[0] == 1:
            # Type 1: repaint reachable cells from x to color c
            x = query[1] - 1  # Convert to 0-indexed
            c = query[2]
            
            # Find all cells reachable from x with the same color
            target_color = colors[x]
            
            # BFS to find all connected cells with the same color
            visited = [False] * N
            stack = [x]
            visited[x] = True
            cells_to_repaint = [x]
            
            while stack:
                curr = stack.pop()
                
                # Check left neighbor
                if curr > 0 and not visited[curr - 1] and colors[curr - 1] == target_color:
                    visited[curr - 1] = True
                    stack.append(curr - 1)
                    cells_to_repaint.append(curr - 1)
                
                # Check right neighbor
                if curr < N - 1 and not visited[curr + 1] and colors[curr + 1] == target_color:
                    visited[curr + 1] = True
                    stack.append(curr + 1)
                    cells_to_repaint.append(curr + 1)
            
            # Repaint all reachable cells
            for cell in cells_to_repaint:
                colors[cell] = c
        
        else:
            # Type 2: count cells with color c
            c = query[1]
            count = sum(1 for color in colors if color == c)
            print(count)

if __name__ == "__main__":
    main()
