#!/usr/bin/env python3

def volume_intersection(cube1, cube2):
    """Calculate volume of intersection of two cubes."""
    a1, b1, c1 = cube1
    a2, b2, c2 = cube2
    
    # Intersection in each dimension
    x_overlap = max(0, min(a1 + 7, a2 + 7) - max(a1, a2))
    y_overlap = max(0, min(b1 + 7, b2 + 7) - max(b1, b2))
    z_overlap = max(0, min(c1 + 7, c2 + 7) - max(c1, c2))
    
    return x_overlap * y_overlap * z_overlap

def calculate_volumes(cubes):
    """
    Calculate V1, V2, V3 for given cube positions.
    Uses inclusion-exclusion principle.
    """
    # Calculate pairwise intersections
    v12 = volume_intersection(cubes[0], cubes[1])
    v13 = volume_intersection(cubes[0], cubes[2])
    v23 = volume_intersection(cubes[1], cubes[2])
    
    # Calculate triple intersection
    a_min = max(cubes[0][0], cubes[1][0], cubes[2][0])
    a_max = min(cubes[0][0] + 7, cubes[1][0] + 7, cubes[2][0] + 7)
    x_overlap = max(0, a_max - a_min)
    
    b_min = max(cubes[0][1], cubes[1][1], cubes[2][1])
    b_max = min(cubes[0][1] + 7, cubes[1][1] + 7, cubes[2][1] + 7)
    y_overlap = max(0, b_max - b_min)
    
    c_min = max(cubes[0][2], cubes[1][2], cubes[2][2])
    c_max = min(cubes[0][2] + 7, cubes[1][2] + 7, cubes[2][2] + 7)
    z_overlap = max(0, c_max - c_min)
    
    v123 = x_overlap * y_overlap * z_overlap
    
    v3 = v123
    v2 = v12 + v13 + v23 - 3 * v123
    v1 = 3 * 343 - 2 * v2 - 3 * v3
    
    return v1, v2, v3

def smart_search(target_v1, target_v2, target_v3):
    """
    Intelligent search based on the constraint and volume relationships.
    """
    # Check constraint: V1 + 2*V2 + 3*V3 = 3*7^3 = 1029
    if target_v1 + 2 * target_v2 + 3 * target_v3 != 1029:
        return None
    
    # Calculate what pairwise volumes sum to
    # v2 = v12 + v13 + v23 - 3*v3
    # So: v12 + v13 + v23 = v2 + 3*v3
    total_pairwise = target_v2 + 3 * target_v3
    
    # Try different distributions of pairwise intersections
    for v12 in range(min(344, total_pairwise + 1)):
        for v13 in range(min(344, total_pairwise - v12 + 1)):
            v23 = total_pairwise - v12 - v13
            if v23 > 343 or v23 < 0:
                continue
            
            # Place C1 at origin
            c1 = (0, 0, 0)
            
            # For C2: try to get intersection v12 with C1
            # Offset by (dx, dy, dz) gives intersection (7-dx)*(7-dy)*(7-dz)
            for dx in range(8):
                for dy in range(8):
                    for dz in range(8):
                        vol_12 = (7 - dx) * (7 - dy) * (7 - dz)
                        if vol_12 == v12:
                            c2 = (dx, dy, dz)
                            
                            # Now search for C3
                            for dx3 in range(8):
                                for dy3 in range(8):
                                    for dz3 in range(8):
                                        vol_13 = (7 - dx3) * (7 - dy3) * (7 - dz3)
                                        if vol_13 == v13:
                                            c3_candidate = (dx3, dy3, dz3)
                                            
                                            # Check v23
                                            vol_23_check = volume_intersection(c2, c3_candidate)
                                            if vol_23_check == v23:
                                                # Verify the full solution
                                                v1, v2, v3 = calculate_volumes([c1, c2, c3_candidate])
                                                if v1 == target_v1 and v2 == target_v2 and v3 == target_v3:
                                                    return [c1, c2, c3_candidate]
    
    return None

def brute_force_search(target_v1, target_v2, target_v3, limit=10):
    """
    Brute force search within a limited range.
    """
    # Check constraint
    if target_v1 + 2 * target_v2 + 3 * target_v3 != 1029:
        return None
    
    # Try different positions
    for a1 in range(-limit, limit + 1):
        for b1 in range(-limit, limit + 1):
            for c1 in range(-limit, limit + 1):
                for a2 in range(-limit, limit + 1):
                    for b2 in range(-limit, limit + 1):
                        for c2 in range(-limit, limit + 1):
                            for a3 in range(-limit, limit + 1):
                                for b3 in range(-limit, limit + 1):
                                    for c3 in range(-limit, limit + 1):
                                        cubes = [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)]
                                        v1, v2, v3 = calculate_volumes(cubes)
                                        if v1 == target_v1 and v2 == target_v2 and v3 == target_v3:
                                            return cubes
    
    return None

def main():
    line = input().strip()
    target_v1, target_v2, target_v3 = map(int, line.split())
    
    # Check the constraint first
    if target_v1 + 2 * target_v2 + 3 * target_v3 != 1029:
        print("No")
        return
    
    # Try smart search first (faster)
    result = smart_search(target_v1, target_v2, target_v3)
    
    # If smart search fails, try brute force with reasonable limits
    if result is None:
        result = brute_force_search(target_v1, target_v2, target_v3, limit=10)
    
    if result is None:
        print("No")
    else:
        print("Yes")
        c1, c2, c3 = result
        print(f"{c1[0]} {c1[1]} {c1[2]} {c2[0]} {c2[1]} {c2[2]} {c3[0]} {c3[1]} {c3[2]}")

if __name__ == "__main__":
    main()
