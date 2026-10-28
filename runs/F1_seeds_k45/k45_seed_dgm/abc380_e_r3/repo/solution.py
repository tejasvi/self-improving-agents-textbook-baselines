import sys

N, Q = map(int, sys.stdin.readline().split())

# color[i] represents the color of cell i (1-indexed)
color = [0] + [i for i in range(1, N + 1)]

for _ in range(Q):
    query = list(map(int, sys.stdin.readline().split()))
    
    if query[0] == 1:
        # Type 1 query: repaint reachable cells
        x, c = query[1], query[2]
        
        # Find all cells reachable from x with the same color
        original_color = color[x]
        
        # Find the leftmost cell with the same color
        left = x
        while left > 1 and color[left - 1] == original_color:
            left -= 1
        
        # Find the rightmost cell with the same color
        right = x
        while right < N and color[right + 1] == original_color:
            right += 1
        
        # Repaint all cells from left to right with color c
        for i in range(left, right + 1):
            color[i] = c
    
    else:
        # Type 2 query: count cells with color c
        c = query[1]
        count = sum(1 for i in range(1, N + 1) if color[i] == c)
        print(count)
