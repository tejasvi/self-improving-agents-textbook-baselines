def read_cuboids():
    """Read N cuboids from stdin."""
    n = int(input())
    cuboids = []
    for _ in range(n):
        coords = list(map(int, input().split()))
        x1, y1, z1, x2, y2, z2 = coords
        # Ensure the ordering is correct
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        cuboids.append(((x1, x2), (y1, y2), (z1, z2)))
    return cuboids


def intervals_overlap(interval1, interval2):
    """
    Check if two 1D intervals overlap with positive length.
    interval1 and interval2 are tuples (a, b) representing [a, b]
    """
    a1, b1 = interval1
    a2, b2 = interval2
    # They overlap with positive length if max(a1, a2) < min(b1, b2)
    return max(a1, a2) < min(b1, b2)


def intervals_are_adjacent(interval1, interval2):
    """
    Check if two 1D intervals are adjacent (touch at boundary).
    One's max equals the other's min.
    """
    a1, b1 = interval1
    a2, b2 = interval2
    return b1 == a2 or b2 == a1


def share_face(cuboid1, cuboid2):
    """
    Check if two cuboids share a face with positive area.
    A face intersection has positive area if:
    - They are adjacent in exactly one dimension
    - They overlap in the other two dimensions
    """
    (x1_min, x1_max), (y1_min, y1_max), (z1_min, z1_max) = cuboid1
    (x2_min, x2_max), (y2_min, y2_max), (z2_min, z2_max) = cuboid2
    
    x_interval1 = (x1_min, x1_max)
    y_interval1 = (y1_min, y1_max)
    z_interval1 = (z1_min, z1_max)
    
    x_interval2 = (x2_min, x2_max)
    y_interval2 = (y2_min, y2_max)
    z_interval2 = (z2_min, z2_max)
    
    # Check each possible face direction
    # Case 1: Adjacent in X, overlap in Y and Z
    if intervals_are_adjacent(x_interval1, x_interval2):
        if intervals_overlap(y_interval1, y_interval2) and intervals_overlap(z_interval1, z_interval2):
            return True
    
    # Case 2: Adjacent in Y, overlap in X and Z
    if intervals_are_adjacent(y_interval1, y_interval2):
        if intervals_overlap(x_interval1, x_interval2) and intervals_overlap(z_interval1, z_interval2):
            return True
    
    # Case 3: Adjacent in Z, overlap in X and Y
    if intervals_are_adjacent(z_interval1, z_interval2):
        if intervals_overlap(x_interval1, x_interval2) and intervals_overlap(y_interval1, y_interval2):
            return True
    
    return False


def main():
    cuboids = read_cuboids()
    n = len(cuboids)
    
    # For each cuboid, count how many others it shares a face with
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j and share_face(cuboids[i], cuboids[j]):
                count += 1
        print(count)


if __name__ == "__main__":
    main()
