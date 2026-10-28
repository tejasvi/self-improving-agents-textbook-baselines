def overlap_1d(a1, a2, b1, b2):
    """Check if two 1D intervals overlap with positive length"""
    return max(a1, b1) < min(a2, b2)


def overlap_2d(rect_a, rect_b):
    """
    Check if two 2D rectangles overlap with positive area.
    Each rectangle is represented as (min1, max1, min2, max2)
    """
    a_min1, a_max1, a_min2, a_max2 = rect_a
    b_min1, b_max1, b_min2, b_max2 = rect_b
    
    return overlap_1d(a_min1, a_max1, b_min1, b_max1) and \
           overlap_1d(a_min2, a_max2, b_min2, b_max2)


def share_face(cuboid_a, cuboid_b):
    """
    Check if two cuboids share a face with positive area.
    Each cuboid is represented as (x1, y1, z1, x2, y2, z2)
    """
    x1a, y1a, z1a, x2a, y2a, z2a = cuboid_a
    x1b, y1b, z1b, x2b, y2b, z2b = cuboid_b
    
    # Check faces perpendicular to x-axis
    # Face of A at x=x2a and face of B at x=x1b
    if x2a == x1b:
        rect_a = (y1a, y2a, z1a, z2a)
        rect_b = (y1b, y2b, z1b, z2b)
        if overlap_2d(rect_a, rect_b):
            return True
    
    # Face of A at x=x1a and face of B at x=x2b
    if x1a == x2b:
        rect_a = (y1a, y2a, z1a, z2a)
        rect_b = (y1b, y2b, z1b, z2b)
        if overlap_2d(rect_a, rect_b):
            return True
    
    # Check faces perpendicular to y-axis
    # Face of A at y=y2a and face of B at y=y1b
    if y2a == y1b:
        rect_a = (x1a, x2a, z1a, z2a)
        rect_b = (x1b, x2b, z1b, z2b)
        if overlap_2d(rect_a, rect_b):
            return True
    
    # Face of A at y=y1a and face of B at y=y2b
    if y1a == y2b:
        rect_a = (x1a, x2a, z1a, z2a)
        rect_b = (x1b, x2b, z1b, z2b)
        if overlap_2d(rect_a, rect_b):
            return True
    
    # Check faces perpendicular to z-axis
    # Face of A at z=z2a and face of B at z=z1b
    if z2a == z1b:
        rect_a = (x1a, x2a, y1a, y2a)
        rect_b = (x1b, x2b, y1b, y2b)
        if overlap_2d(rect_a, rect_b):
            return True
    
    # Face of A at z=z1a and face of B at z=z2b
    if z1a == z2b:
        rect_a = (x1a, x2a, y1a, y2a)
        rect_b = (x1b, x2b, y1b, y2b)
        if overlap_2d(rect_a, rect_b):
            return True
    
    return False


def main():
    n = int(input())
    cuboids = []
    for _ in range(n):
        coords = list(map(int, input().split()))
        cuboids.append(coords)
    
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j and share_face(cuboids[i], cuboids[j]):
                count += 1
        print(count)


if __name__ == "__main__":
    main()
