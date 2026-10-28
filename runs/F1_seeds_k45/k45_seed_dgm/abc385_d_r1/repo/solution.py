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
    
    # Track current position
    x, y = Sx, Sy
    
    # Track which houses we've visited
    visited = set()
    
    # Process each movement
    for direction, distance in movements:
        # Determine the next position
        if direction == 'U':
            next_x, next_y = x, y + distance
        elif direction == 'D':
            next_x, next_y = x, y - distance
        elif direction == 'L':
            next_x, next_y = x - distance, y
        elif direction == 'R':
            next_x, next_y = x + distance, y
        
        # Check which houses lie on the path from (x, y) to (next_x, next_y)
        for house_x, house_y in houses:
            # Check if the house is on this segment
            if direction in ['U', 'D']:
                # Vertical movement, x coordinate stays the same
                if house_x == x:
                    # Check if house_y is between y and next_y
                    min_y = min(y, next_y)
                    max_y = max(y, next_y)
                    if min_y <= house_y <= max_y:
                        visited.add((house_x, house_y))
            else:  # direction in ['L', 'R']
                # Horizontal movement, y coordinate stays the same
                if house_y == y:
                    # Check if house_x is between x and next_x
                    min_x = min(x, next_x)
                    max_x = max(x, next_x)
                    if min_x <= house_x <= max_x:
                        visited.add((house_x, house_y))
        
        # Update current position
        x, y = next_x, next_y
    
    # Output
    print(x, y, len(visited))

solve()
