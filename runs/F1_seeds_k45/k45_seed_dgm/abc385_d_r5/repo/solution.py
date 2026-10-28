# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    N, M, Sx, Sy = map(int, input().split())
    
    houses = []
    for _ in range(N):
        x, y = map(int, input().split())
        houses.append((x, y))
    
    movements = []
    for _ in range(M):
        parts = input().split()
        direction = parts[0]
        distance = int(parts[1])
        movements.append((direction, distance))
    
    # Track visited houses
    visited_houses = set()
    
    # Current position
    x, y = Sx, Sy
    
    # Process each movement
    for direction, distance in movements:
        # Calculate new position
        if direction == 'U':
            new_x, new_y = x, y + distance
        elif direction == 'D':
            new_x, new_y = x, y - distance
        elif direction == 'L':
            new_x, new_y = x - distance, y
        elif direction == 'R':
            new_x, new_y = x + distance, y
        
        # Check which houses are on this path
        for hx, hy in houses:
            # For horizontal movement (U/D): y stays same, x changes
            if direction in ['U', 'D']:
                # House is on path if hx == x and hy is between y and new_y
                if hx == x:
                    if min(y, new_y) <= hy <= max(y, new_y):
                        visited_houses.add((hx, hy))
            # For vertical movement (L/R): x stays same, y changes
            else:  # direction in ['L', 'R']
                # House is on path if hy == y and hx is between x and new_x
                if hy == y:
                    if min(x, new_x) <= hx <= max(x, new_x):
                        visited_houses.add((hx, hy))
        
        # Update position
        x, y = new_x, new_y
    
    # Output final position and count of visited houses
    print(x, y, len(visited_houses))

solve()
