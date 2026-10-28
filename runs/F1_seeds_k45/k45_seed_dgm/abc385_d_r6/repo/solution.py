# Read input
N, M, Sx, Sy = map(int, input().split())

houses = []
for _ in range(N):
    x, y = map(int, input().split())
    houses.append((x, y))

moves = []
for _ in range(M):
    parts = input().split()
    direction = parts[0]
    distance = int(parts[1])
    moves.append((direction, distance))

# Track current position
current_x = Sx
current_y = Sy

# Track visited houses
visited_houses = set()

# Process each move
for direction, distance in moves:
    start_x, start_y = current_x, current_y
    
    if direction == 'U':
        end_x, end_y = current_x, current_y + distance
    elif direction == 'D':
        end_x, end_y = current_x, current_y - distance
    elif direction == 'L':
        end_x, end_y = current_x - distance, current_y
    elif direction == 'R':
        end_x, end_y = current_x + distance, current_y
    
    # Check which houses are on this line segment
    for house_x, house_y in houses:
        # Check if house is on the line segment
        if direction in ['U', 'D']:  # Vertical movement
            # Check if house is on the same vertical line
            if house_x == current_x:
                # Check if house is between start and end
                min_y = min(start_y, end_y)
                max_y = max(start_y, end_y)
                if min_y <= house_y <= max_y:
                    visited_houses.add((house_x, house_y))
        else:  # Horizontal movement (L or R)
            # Check if house is on the same horizontal line
            if house_y == current_y:
                # Check if house is between start and end
                min_x = min(start_x, end_x)
                max_x = max(start_x, end_x)
                if min_x <= house_x <= max_x:
                    visited_houses.add((house_x, house_y))
    
    # Update current position
    current_x = end_x
    current_y = end_y

# Output
print(current_x, current_y, len(visited_houses))
