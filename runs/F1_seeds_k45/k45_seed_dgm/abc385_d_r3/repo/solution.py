#!/usr/bin/env python3

def main():
    # Read input
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
        parts = input().split()
        direction = parts[0]
        distance = int(parts[1])
        movements.append((direction, distance))
    
    # Track current position and visited houses
    x, y = S_x, S_y
    visited_houses = set()
    
    # Process each movement
    for direction, distance in movements:
        # Determine the movement vector
        if direction == 'U':
            dx, dy = 0, 1
        elif direction == 'D':
            dx, dy = 0, -1
        elif direction == 'L':
            dx, dy = -1, 0
        elif direction == 'R':
            dx, dy = 1, 0
        
        # Check which houses are on this path
        for house_x, house_y in houses:
            if (house_x, house_y) not in visited_houses:
                # Check if this house is on the path from (x, y) to (x + dx*distance, y + dy*distance)
                # The house must be on the line segment
                
                if dx != 0:  # Horizontal movement
                    # y coordinate must match
                    if house_y == y:
                        # Check if house_x is between x and x + dx*distance
                        if dx > 0:
                            if x < house_x <= x + distance:
                                visited_houses.add((house_x, house_y))
                        else:  # dx < 0
                            if x + distance <= house_x < x:
                                visited_houses.add((house_x, house_y))
                
                else:  # dy != 0, vertical movement
                    # x coordinate must match
                    if house_x == x:
                        # Check if house_y is between y and y + dy*distance
                        if dy > 0:
                            if y < house_y <= y + distance:
                                visited_houses.add((house_x, house_y))
                        else:  # dy < 0
                            if y + distance <= house_y < y:
                                visited_houses.add((house_x, house_y))
        
        # Update position
        x += dx * distance
        y += dy * distance
    
    # Output
    print(x, y, len(visited_houses))

if __name__ == "__main__":
    main()
