# Write your solution here. Read from stdin, write to stdout.

def main():
    # Read input
    N, M, S_x, S_y = map(int, input().split())
    
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
    
    # Track Santa's current position
    current_x, current_y = S_x, S_y
    
    # Track which houses have been visited
    visited_houses = set()
    
    # Process each movement
    for direction, distance in movements:
        # Determine next position
        if direction == 'U':
            next_x, next_y = current_x, current_y + distance
        elif direction == 'D':
            next_x, next_y = current_x, current_y - distance
        elif direction == 'L':
            next_x, next_y = current_x - distance, current_y
        elif direction == 'R':
            next_x, next_y = current_x + distance, current_y
        
        # Check which houses are on this line segment
        for house_x, house_y in houses:
            # Check if house is on the path
            if direction == 'U':
                # Moving up: x stays same, y increases
                if house_x == current_x and min(current_y, next_y) <= house_y <= max(current_y, next_y):
                    visited_houses.add((house_x, house_y))
            elif direction == 'D':
                # Moving down: x stays same, y decreases
                if house_x == current_x and min(current_y, next_y) <= house_y <= max(current_y, next_y):
                    visited_houses.add((house_x, house_y))
            elif direction == 'L':
                # Moving left: y stays same, x decreases
                if house_y == current_y and min(current_x, next_x) <= house_x <= max(current_x, next_x):
                    visited_houses.add((house_x, house_y))
            elif direction == 'R':
                # Moving right: y stays same, x increases
                if house_y == current_y and min(current_x, next_x) <= house_x <= max(current_x, next_x):
                    visited_houses.add((house_x, house_y))
        
        # Move to next position
        current_x, current_y = next_x, next_y
    
    # Output results
    print(f"{current_x} {current_y} {len(visited_houses)}")

if __name__ == "__main__":
    main()
