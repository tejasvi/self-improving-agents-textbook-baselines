def intervals_overlap(a1, a2, b1, b2):
    """Check if two 1D intervals [a1, a2) and [b1, b2) have non-empty intersection"""
    return max(a1, b1) < min(a2, b2)

def rectangles_overlap(x1_min, x1_max, y1_min, y1_max, x2_min, x2_max, y2_min, y2_max):
    """Check if two rectangles in a 2D plane have non-empty intersection"""
    x_overlap = intervals_overlap(x1_min, x1_max, x2_min, x2_max)
    y_overlap = intervals_overlap(y1_min, y1_max, y2_min, y2_max)
    return x_overlap and y_overlap

def share_face(cuboid1, cuboid2):
    """
    Check if two cuboids share a face.
    cuboid is (x_min, y_min, z_min, x_max, y_max, z_max)
    """
    x1_min, y1_min, z1_min, x1_max, y1_max, z1_max = cuboid1
    x2_min, y2_min, z2_min, x2_max, y2_max, z2_max = cuboid2
    
    # Check if they share a face perpendicular to x-axis
    if x1_max == x2_min or x1_min == x2_max:
        # They touch along the x direction
        # Check if they overlap in y-z plane
        if rectangles_overlap(y1_min, y1_max, z1_min, z1_max, 
                             y2_min, y2_max, z2_min, z2_max):
            return True
    
    # Check if they share a face perpendicular to y-axis
    if y1_max == y2_min or y1_min == y2_max:
        # They touch along the y direction
        # Check if they overlap in x-z plane
        if rectangles_overlap(x1_min, x1_max, z1_min, z1_max,
                             x2_min, x2_max, z2_min, z2_max):
            return True
    
    # Check if they share a face perpendicular to z-axis
    if z1_max == z2_min or z1_min == z2_max:
        # They touch along the z direction
        # Check if they overlap in x-y plane
        if rectangles_overlap(x1_min, x1_max, y1_min, y1_max,
                             x2_min, x2_max, y2_min, y2_max):
            return True
    
    return False

# Read input
n = int(input())
cuboids = []
for _ in range(n):
    coords = list(map(int, input().split()))
    x1, y1, z1, x2, y2, z2 = coords
    # Normalize so that first point is min and second is max
    cuboid = (min(x1, x2), min(y1, y2), min(z1, z2),
              max(x1, x2), max(y1, y2), max(z1, z2))
    cuboids.append(cuboid)

# For each cuboid, count how many others it shares a face with
for i in range(n):
    count = 0
    for j in range(n):
        if i != j and share_face(cuboids[i], cuboids[j]):
            count += 1
    print(count)
