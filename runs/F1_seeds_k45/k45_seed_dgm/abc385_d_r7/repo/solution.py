def read_input():
    # Read first line: N M S_x S_y
    line = input().split()
    N, M, S_x, S_y = int(line[0]), int(line[1]), int(line[2]), int(line[3])
    
    # Read houses
    houses = []
    for _ in range(N):
        x, y = map(int, input().split())
        houses.append((x, y))
    
    # Read movements
    movements = []
    for _ in range(M):
        line = input().split()
        direction = line[0]
        distance = int(line[1])
        movements.append((direction, distance))
    
    return N, M, S_x, S_y, houses, movements


def point_on_segment(px, py, x1, y1, x2, y2):
    """
    Check if point (px, py) lies on the line segment from (x1, y1) to (x2, y2)
    """
    # Check if point is within bounding box
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    
    if not (min_x <= px <= max_x and min_y <= py <= max_y):
        return False
    
    # Check if point is collinear with the segment
    # For a segment from (x1, y1) to (x2, y2):
    # If horizontal (y1 == y2), then py must equal y1 and x1 <= px <= x2
    # If vertical (x1 == x2), then px must equal x1 and y1 <= py <= y2
    
    if x1 == x2:  # Vertical segment
        return px == x1
    elif y1 == y2:  # Horizontal segment
        return py == y1
    else:
        # Should not happen given the problem constraints (only U/D/L/R movements)
        return False


def solve():
    N, M, S_x, S_y, houses, movements = read_input()
    
    # Track visited houses
    visited = set()
    
    # Current position
    x, y = S_x, S_y
    
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
        
        # Check which houses are on this segment
        for house_x, house_y in houses:
            if point_on_segment(house_x, house_y, x, y, new_x, new_y):
                visited.add((house_x, house_y))
        
        # Update current position
        x, y = new_x, new_y
    
    # Output: final position and count of visited houses
    print(x, y, len(visited))


solve()
