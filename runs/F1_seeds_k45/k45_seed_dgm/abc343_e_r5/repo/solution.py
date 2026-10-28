def solve():
    V1, V2, V3 = map(int, input().split())
    
    # Check the necessary condition: V1 + 2*V2 + 3*V3 = 3 * 7^3 = 1029
    if V1 + 2*V2 + 3*V3 != 1029:
        print("No")
        return
    
    # Try to construct a valid placement
    # Strategy: Use systematic overlaps
    
    # We can parameterize overlaps in each dimension:
    # If cubes i and j overlap in dimension d, let overlap_d be the overlap size
    # 
    # For simplicity, let's try different patterns of overlaps
    
    CUBE_SIZE = 7
    
    # Try all possible overlap patterns
    # We'll try different ways to overlap the cubes
    
    # Pattern: Try overlapping in specific dimensions
    # Let's parameterize by overlap sizes in x, y, z dimensions
    
    for ox in range(8):  # overlap in x between cubes (0 to 7)
        for oy in range(8):  # overlap in y 
            for oz in range(8):  # overlap in z
                # Try configuration where:
                # C1 at (0, 0, 0)
                # C2 at (7-ox, 7-oy, 0)  - overlaps with C1 by ox in x, oy in y, 0 in z
                # C3 at (0, 0, 7-oz)      - overlaps with C1 by 0 in x, 0 in y, oz in z
                
                result = check_config(0, 0, 0, 
                                     7-ox, 7-oy, 0,
                                     0, 0, 7-oz,
                                     V1, V2, V3)
                if result:
                    print("Yes")
                    print(result)
                    return
    
    # Try another pattern
    for ox in range(8):
        for oy in range(8):
            for oz in range(8):
                # C1 at (0, 0, 0)
                # C2 at (7-ox, 0, 7-oy)
                # C3 at (0, 7-oz, 0)
                
                result = check_config(0, 0, 0,
                                     7-ox, 0, 7-oy,
                                     0, 7-oz, 0,
                                     V1, V2, V3)
                if result:
                    print("Yes")
                    print(result)
                    return
    
    # Try more patterns
    for ox in range(8):
        for oy in range(8):
            for oz in range(8):
                # C1 at (0, 0, 0)
                # C2 at (7-ox, 0, 0)
                # C3 at (0, 7-oy, 7-oz)
                
                result = check_config(0, 0, 0,
                                     7-ox, 0, 0,
                                     0, 7-oy, 7-oz,
                                     V1, V2, V3)
                if result:
                    print("Yes")
                    print(result)
                    return
    
    print("No")

def check_config(a1, b1, c1, a2, b2, c2, a3, b3, c3, V1, V2, V3):
    """Check if this configuration gives the desired volumes"""
    
    # Calculate overlaps
    v1, v2, v3 = calculate_volumes(a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    if v1 == V1 and v2 == V2 and v3 == V3:
        return f"{a1} {b1} {c1} {a2} {b2} {c2} {a3} {b3} {c3}"
    return None

def calculate_volumes(a1, b1, c1, a2, b2, c2, a3, b3, c3):
    """Calculate V1, V2, V3 for the given cube configuration"""
    
    CUBE_SIZE = 7
    
    # We need to calculate the volume of regions containing exactly 1, 2, 3 cubes
    # Use inclusion-exclusion
    
    # Volume of each cube
    vol_c1 = CUBE_SIZE ** 3
    vol_c2 = CUBE_SIZE ** 3
    vol_c3 = CUBE_SIZE ** 3
    
    # Volume of pairwise intersections
    vol_c1_c2 = intersection_volume(a1, b1, c1, a2, b2, c2)
    vol_c1_c3 = intersection_volume(a1, b1, c1, a3, b3, c3)
    vol_c2_c3 = intersection_volume(a2, b2, c2, a3, b3, c3)
    
    # Volume of triple intersection
    vol_c1_c2_c3 = intersection_volume_3(a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    # By inclusion-exclusion:
    # V_3 = volume in all 3
    # V_2 = (vol_c1_c2 - vol_c1_c2_c3) + (vol_c1_c3 - vol_c1_c2_c3) + (vol_c2_c3 - vol_c1_c2_c3)
    #     = vol_c1_c2 + vol_c1_c3 + vol_c2_c3 - 3*vol_c1_c2_c3
    # V_1 = vol_c1 + vol_c2 + vol_c3 - 2*vol_c1_c2 - 2*vol_c1_c3 - 2*vol_c2_c3 + 3*vol_c1_c2_c3
    
    v3 = vol_c1_c2_c3
    v2 = vol_c1_c2 + vol_c1_c3 + vol_c2_c3 - 3 * vol_c1_c2_c3
    v1 = vol_c1 + vol_c2 + vol_c3 - 2*(vol_c1_c2 + vol_c1_c3 + vol_c2_c3) + 3*vol_c1_c2_c3
    
    return v1, v2, v3

def intersection_volume(a1, b1, c1, a2, b2, c2):
    """Calculate intersection volume of two cubes"""
    CUBE_SIZE = 7
    
    # Intersection in x dimension
    x_intersect = max(0, min(a1 + CUBE_SIZE, a2 + CUBE_SIZE) - max(a1, a2))
    y_intersect = max(0, min(b1 + CUBE_SIZE, b2 + CUBE_SIZE) - max(b1, b2))
    z_intersect = max(0, min(c1 + CUBE_SIZE, c2 + CUBE_SIZE) - max(c1, c2))
    
    return x_intersect * y_intersect * z_intersect

def intersection_volume_3(a1, b1, c1, a2, b2, c2, a3, b3, c3):
    """Calculate intersection volume of three cubes"""
    CUBE_SIZE = 7
    
    x_min = max(a1, a2, a3)
    x_max = min(a1 + CUBE_SIZE, a2 + CUBE_SIZE, a3 + CUBE_SIZE)
    x_intersect = max(0, x_max - x_min)
    
    y_min = max(b1, b2, b3)
    y_max = min(b1 + CUBE_SIZE, b2 + CUBE_SIZE, b3 + CUBE_SIZE)
    y_intersect = max(0, y_max - y_min)
    
    z_min = max(c1, c2, c3)
    z_max = min(c1 + CUBE_SIZE, c2 + CUBE_SIZE, c3 + CUBE_SIZE)
    z_intersect = max(0, z_max - z_min)
    
    return x_intersect * y_intersect * z_intersect

if __name__ == "__main__":
    solve()
