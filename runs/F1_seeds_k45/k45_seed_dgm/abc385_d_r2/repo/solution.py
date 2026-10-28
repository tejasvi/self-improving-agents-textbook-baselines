def solve():
    # Read input
    line1 = input().split()
    N, M = int(line1[0]), int(line1[1])
    S_x, S_y = int(line1[2]), int(line1[3])
    
    houses = []
    for _ in range(N):
        x, y = map(int, input().split())
        houses.append((x, y))
    
    commands = []
    for _ in range(M):
        parts = input().split()
        direction = parts[0]
        distance = int(parts[1])
        commands.append((direction, distance))
    
    # Process movements
    current_x, current_y = S_x, S_y
    visited_houses = set()
    
    for direction, distance in commands:
        # Calculate next position
        if direction == 'U':
            next_x, next_y = current_x, current_y + distance
        elif direction == 'D':
            next_x, next_y = current_x, current_y - distance
        elif direction == 'L':
            next_x, next_y = current_x - distance, current_y
        elif direction == 'R':
            next_x, next_y = current_x + distance, current_y
        
        # Check which houses are on this path
        for house_x, house_y in houses:
            # Check if house is on the path from (current_x, current_y) to (next_x, next_y)
            
            if direction == 'U' or direction == 'D':
                # Moving vertically, y changes, x stays same
                if house_x == current_x:
                    # House is on the same vertical line
                    min_y = min(current_y, next_y)
                    max_y = max(current_y, next_y)
                    if min_y <= house_y <= max_y:
                        visited_houses.add((house_x, house_y))
            else:  # direction == 'L' or direction == 'R'
                # Moving horizontally, x changes, y stays same
                if house_y == current_y:
                    # House is on the same horizontal line
                    min_x = min(current_x, next_x)
                    max_x = max(current_x, next_x)
                    if min_x <= house_x <= max_x:
                        visited_houses.add((house_x, house_y))
        
        # Update current position
        current_x, current_y = next_x, next_y
    
    # Output result
    print(current_x, current_y, len(visited_houses))

solve()
