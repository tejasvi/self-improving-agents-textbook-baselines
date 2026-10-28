# Read input
line = input().split()
N, M, S_x, S_y = int(line[0]), int(line[1]), int(line[2]), int(line[3])

houses = []
for _ in range(N):
    line = input().split()
    x, y = int(line[0]), int(line[1])
    houses.append((x, y))

movements = []
for _ in range(M):
    line = input().split()
    direction = line[0]
    distance = int(line[1])
    movements.append((direction, distance))

# Track which houses we've visited
visited_houses = set()

# Current position
x, y = S_x, S_y

# Process each movement
for direction, distance in movements:
    # Determine start and end positions
    if direction == 'U':
        start_pos = (x, y)
        end_pos = (x, y + distance)
        # Check which houses are on the vertical line at x
        for house_x, house_y in houses:
            if house_x == x and min(y, y + distance) <= house_y <= max(y, y + distance):
                visited_houses.add((house_x, house_y))
        y += distance
    elif direction == 'D':
        start_pos = (x, y)
        end_pos = (x, y - distance)
        # Check which houses are on the vertical line at x
        for house_x, house_y in houses:
            if house_x == x and min(y - distance, y) <= house_y <= max(y - distance, y):
                visited_houses.add((house_x, house_y))
        y -= distance
    elif direction == 'L':
        start_pos = (x, y)
        end_pos = (x - distance, y)
        # Check which houses are on the horizontal line at y
        for house_x, house_y in houses:
            if house_y == y and min(x - distance, x) <= house_x <= max(x - distance, x):
                visited_houses.add((house_x, house_y))
        x -= distance
    elif direction == 'R':
        start_pos = (x, y)
        end_pos = (x + distance, y)
        # Check which houses are on the horizontal line at y
        for house_x, house_y in houses:
            if house_y == y and min(x, x + distance) <= house_x <= max(x, x + distance):
                visited_houses.add((house_x, house_y))
        x += distance

# Output final position and count of distinct houses visited
print(x, y, len(visited_houses))
