def read_input():
    n = int(input())
    cuboids = []
    for _ in range(n):
        coords = list(map(int, input().split()))
        x1, y1, z1, x2, y2, z2 = coords
        # Normalize so that first point is min
        cuboids.append((
            min(x1, x2), max(x1, x2),
            min(y1, y2), max(y1, y2),
            min(z1, z2), max(z1, z2)
        ))
    return cuboids

def intersect_1d(a1, a2, b1, b2):
    """Returns the overlap length of two 1D intervals [a1, a2] and [b1, b2]"""
    return max(0, min(a2, b2) - max(a1, b1))

def intersect_2d_area(x1_a, x2_a, y1_a, y2_a, x1_b, x2_b, y1_b, y2_b):
    """Returns the area of 2D rectangular overlap"""
    dx = intersect_1d(x1_a, x2_a, x1_b, x2_b)
    dy = intersect_1d(y1_a, y2_a, y1_b, y2_b)
    return dx * dy

def shares_face(cuboid_i, cuboid_j):
    """Check if two cuboids share a face (positive area intersection on surface)"""
    x1_i, x2_i, y1_i, y2_i, z1_i, z2_i = cuboid_i
    x1_j, x2_j, y1_j, y2_j, z1_j, z2_j = cuboid_j
    
    # Check face at x = x2_i with x = x1_j
    if x2_i == x1_j:
        area = intersect_2d_area(y1_i, y2_i, z1_i, z2_i, y1_j, y2_j, z1_j, z2_j)
        if area > 0:
            return True
    
    # Check face at x = x1_i with x = x2_j
    if x1_i == x2_j:
        area = intersect_2d_area(y1_i, y2_i, z1_i, z2_i, y1_j, y2_j, z1_j, z2_j)
        if area > 0:
            return True
    
    # Check face at y = y2_i with y = y1_j
    if y2_i == y1_j:
        area = intersect_2d_area(x1_i, x2_i, z1_i, z2_i, x1_j, x2_j, z1_j, z2_j)
        if area > 0:
            return True
    
    # Check face at y = y1_i with y = y2_j
    if y1_i == y2_j:
        area = intersect_2d_area(x1_i, x2_i, z1_i, z2_i, x1_j, x2_j, z1_j, z2_j)
        if area > 0:
            return True
    
    # Check face at z = z2_i with z = z1_j
    if z2_i == z1_j:
        area = intersect_2d_area(x1_i, x2_i, y1_i, y2_i, x1_j, x2_j, y1_j, y2_j)
        if area > 0:
            return True
    
    # Check face at z = z1_i with z = z2_j
    if z1_i == z2_j:
        area = intersect_2d_area(x1_i, x2_i, y1_i, y2_i, x1_j, x2_j, y1_j, y2_j)
        if area > 0:
            return True
    
    return False

def solve():
    cuboids = read_input()
    n = len(cuboids)
    
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j and shares_face(cuboids[i], cuboids[j]):
                count += 1
        print(count)

if __name__ == "__main__":
    solve()
