def get_intersection_volume(cube1, cube2):
    """
    Calculate the volume of intersection between two cubes.
    cube format: (a, b, c) representing [a, a+7] x [b, b+7] x [c, c+7]
    """
    a1, b1, c1 = cube1
    a2, b2, c2 = cube2
    
    # Calculate overlap in each dimension
    x_overlap = max(0, min(a1 + 7, a2 + 7) - max(a1, a2))
    y_overlap = max(0, min(b1 + 7, b2 + 7) - max(b1, b2))
    z_overlap = max(0, min(c1 + 7, c2 + 7) - max(c1, c2))
    
    return x_overlap * y_overlap * z_overlap


def count_volumes(cubes):
    """
    Count volumes of regions in exactly 1, 2, and 3 cubes.
    Returns (V1, V2, V3)
    """
    c1, c2, c3 = cubes
    
    # Pairwise intersections
    v12 = get_intersection_volume(c1, c2)
    v13 = get_intersection_volume(c1, c3)
    v23 = get_intersection_volume(c2, c3)
    
    # Triple intersection
    a1, b1, c_1 = c1
    a2, b2, c_2 = c2
    a3, b3, c_3 = c3
    
    x_min = max(a1, a2, a3)
    x_max = min(a1 + 7, a2 + 7, a3 + 7)
    y_min = max(b1, b2, b3)
    y_max = min(b1 + 7, b2 + 7, b3 + 7)
    z_min = max(c_1, c_2, c_3)
    z_max = min(c_1 + 7, c_2 + 7, c_3 + 7)
    
    v123 = max(0, x_max - x_min) * max(0, y_max - y_min) * max(0, z_max - z_min)
    
    # Volume in exactly 2: (v12 - v123) + (v13 - v123) + (v23 - v123)
    v2 = v12 + v13 + v23 - 3 * v123
    
    # Volume in exactly 1: 1029 - v12 - v13 - v23 + 2*v123
    v1 = 1029 - v12 - v13 - v23 + 2 * v123
    
    return v1, v2, v123


def solve(V1, V2, V3):
    """
    Try to find three cube positions that satisfy the volume constraints.
    """
    
    # Check necessary condition
    if V1 + 2 * V2 + 3 * V3 != 1029:
        return None
    
    # Try different configurations
    # Strategy: vary overlaps in each dimension
    for offset_x in range(-7, 8):
        for offset_y in range(-7, 8):
            for offset_z in range(-7, 8):
                # Cube 1 at origin
                c1 = (0, 0, 0)
                # Cube 2 at offset
                c2 = (offset_x, offset_y, offset_z)
                
                # For each pair, try to find c3
                for offset_x3 in range(-7, 8):
                    for offset_y3 in range(-7, 8):
                        for offset_z3 in range(-7, 8):
                            c3 = (offset_x3, offset_y3, offset_z3)
                            
                            v1, v2, v3 = count_volumes((c1, c2, c3))
                            if v1 == V1 and v2 == V2 and v3 == V3:
                                # Check coordinate bounds
                                if all(abs(coord) <= 100 for cube in [c1, c2, c3] for coord in cube):
                                    return (c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], c3[0], c3[1], c3[2])
    
    return None


V1, V2, V3 = map(int, input().split())

result = solve(V1, V2, V3)
if result:
    print("Yes")
    print(*result)
else:
    print("No")
