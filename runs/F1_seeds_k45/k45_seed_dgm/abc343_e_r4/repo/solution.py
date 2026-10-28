def compute_intersection_volume(c1, c2):
    """Compute volume of intersection of two cubes"""
    # c1 = (a1, b1, c1), c2 = (a2, b2, c2)
    # Cube 1: [a1, a1+7] x [b1, b1+7] x [c1, c1+7]
    # Cube 2: [a2, a2+7] x [b2, b2+7] x [c2, c2+7]
    a1, b1, c1_val = c1
    a2, b2, c2_val = c2
    
    # For each dimension, compute overlap length
    def overlap_length(start1, start2, size=7):
        end1 = start1 + size
        end2 = start2 + size
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        return max(0, overlap_end - overlap_start)
    
    dx = overlap_length(a1, a2)
    dy = overlap_length(b1, b2)
    dz = overlap_length(c1_val, c2_val)
    
    return dx * dy * dz

def compute_volumes_exact(cubes):
    """Compute exact volumes using inclusion-exclusion"""
    c1, c2, c3 = cubes
    
    # Volume of each cube
    vol1 = vol2 = vol3 = 343
    
    # Intersections of pairs
    i12 = compute_intersection_volume(c1, c2)
    i13 = compute_intersection_volume(c1, c3)
    i23 = compute_intersection_volume(c2, c3)
    
    # Intersection of all three
    a1, b1, c1_val = c1
    a2, b2, c2_val = c2
    a3, b3, c3_val = c3
    
    def overlap_length(start1, start2, size=7):
        end1 = start1 + size
        end2 = start2 + size
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        return max(0, overlap_end - overlap_start)
    
    # Find intersection region of all three
    x_min = max(a1, a2, a3)
    x_max = min(a1 + 7, a2 + 7, a3 + 7)
    y_min = max(b1, b2, b3)
    y_max = min(b1 + 7, b2 + 7, b3 + 7)
    z_min = max(c1_val, c2_val, c3_val)
    z_max = min(c1_val + 7, c2_val + 7, c3_val + 7)
    
    i123 = max(0, x_max - x_min) * max(0, y_max - y_min) * max(0, z_max - z_min)
    
    # Standard inclusion-exclusion for volumes
    # Points in exactly 1 = vol1 + vol2 + vol3 - 2*(i12 + i13 + i23) + 3*i123
    # Points in exactly 2 = i12 + i13 + i23 - 3*i123
    # Points in all 3 = i123
    
    v1 = vol1 + vol2 + vol3 - 2 * (i12 + i13 + i23) + 3 * i123
    v2 = i12 + i13 + i23 - 3 * i123
    v3 = i123
    
    return v1, v2, v3

def solve(v1_target, v2_target, v3_target):
    """Try to find cube positions"""
    # Constraint: v1 + 2*v2 + 3*v3 = 1029
    if v1_target + 2 * v2_target + 3 * v3_target != 1029:
        return None
    
    # Strategy: try different overlap patterns
    # Start with simple configurations
    
    # Try all positions with small offsets (0 to 7 in each dimension)
    for offset_a in range(0, 8):
        for offset_b in range(0, 8):
            for offset_c in range(0, 8):
                # Cube 1 at origin
                c1 = (0, 0, 0)
                # Cube 2 offset from cube 1
                c2 = (offset_a, offset_b, offset_c)
                
                # For cube 3, try different offsets
                for offset_a2 in range(0, 8):
                    for offset_b2 in range(0, 8):
                        for offset_c2 in range(0, 8):
                            c3 = (offset_a2, offset_b2, offset_c2)
                            
                            v1, v2, v3 = compute_volumes_exact([c1, c2, c3])
                            if v1 == v1_target and v2 == v2_target and v3 == v3_target:
                                return (c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], c3[0], c3[1], c3[2])
    
    return None

# Read input
v1, v2, v3 = map(int, input().split())

# Try to solve
result = solve(v1, v2, v3)

if result:
    print("Yes")
    print(*result)
else:
    print("No")
