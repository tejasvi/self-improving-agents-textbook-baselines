def intervals_overlap(a1, a2, b1, b2):
    """Check if two 1D intervals [a1, a2] and [b1, b2] overlap with positive length."""
    return max(a1, b1) < min(a2, b2)


def cuboids_share_face(cuboid1, cuboid2):
    """
    Check if two cuboids share a face.
    Each cuboid is represented as (x1, y1, z1, x2, y2, z2)
    """
    x1_1, y1_1, z1_1, x2_1, y2_1, z2_1 = cuboid1
    x1_2, y1_2, z1_2, x2_2, y2_2, z2_2 = cuboid2
    
    # Check if they are adjacent along X-axis and overlap in Y and Z
    if x2_1 == x1_2 or x2_2 == x1_1:
        if intervals_overlap(y1_1, y2_1, y1_2, y2_2) and intervals_overlap(z1_1, z2_1, z1_2, z2_2):
            return True
    
    # Check if they are adjacent along Y-axis and overlap in X and Z
    if y2_1 == y1_2 or y2_2 == y1_1:
        if intervals_overlap(x1_1, x2_1, x1_2, x2_2) and intervals_overlap(z1_1, z2_1, z1_2, z2_2):
            return True
    
    # Check if they are adjacent along Z-axis and overlap in X and Y
    if z2_1 == z1_2 or z2_2 == z1_1:
        if intervals_overlap(x1_1, x2_1, x1_2, x2_2) and intervals_overlap(y1_1, y2_1, y1_2, y2_2):
            return True
    
    return False


def main():
    n = int(input())
    cuboids = []
    
    for _ in range(n):
        coords = list(map(int, input().split()))
        x1, y1, z1, x2, y2, z2 = coords
        # Ensure proper ordering
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1
        cuboids.append((x1, y1, z1, x2, y2, z2))
    
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j:
                if cuboids_share_face(cuboids[i], cuboids[j]):
                    count += 1
        print(count)


if __name__ == "__main__":
    main()
