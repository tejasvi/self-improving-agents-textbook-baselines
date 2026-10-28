#!/usr/bin/env python3

def intersect_interval(a1, b1, a2, b2):
    """Find intersection length of two intervals [a1, b1] and [a2, b2]"""
    start = max(a1, a2)
    end = min(b1, b2)
    if start >= end:
        return 0
    return end - start

def cube_intersection_volume(cube1, cube2):
    """Calculate volume of intersection of two cubes"""
    a1, b1, c1 = cube1
    a2, b2, c2 = cube2
    
    dx = intersect_interval(a1, a1+7, a2, a2+7)
    dy = intersect_interval(b1, b1+7, b2, b2+7)
    dz = intersect_interval(c1, c1+7, c2, c2+7)
    
    return dx * dy * dz

def count_volumes(cube1, cube2, cube3):
    """
    Calculate V1, V2, V3 for three cubes.
    V1: volume in exactly 1 cube
    V2: volume in exactly 2 cubes
    V3: volume in all 3 cubes
    """
    a1, b1, c1 = cube1
    a2, b2, c2 = cube2
    a3, b3, c3 = cube3
    
    # Calculate pairwise intersections
    v12 = cube_intersection_volume(cube1, cube2)
    v13 = cube_intersection_volume(cube1, cube3)
    v23 = cube_intersection_volume(cube2, cube3)
    
    # Calculate triple intersection
    x_start = max(a1, a2, a3)
    x_end = min(a1+7, a2+7, a3+7)
    dx = max(0, x_end - x_start)
    
    y_start = max(b1, b2, b3)
    y_end = min(b1+7, b2+7, b3+7)
    dy = max(0, y_end - y_start)
    
    z_start = max(c1, c2, c3)
    z_end = min(c1+7, c2+7, c3+7)
    dz = max(0, z_end - z_start)
    
    v123 = dx * dy * dz
    
    # Calculate regions with exactly k cubes
    # Exactly 2 cubes: intersection of pairs minus triple intersection
    v12_only = v12 - v123
    v13_only = v13 - v123
    v23_only = v23 - v123
    
    # Exactly 1 cube
    only_c1 = 343 - v12_only - v13_only - v123
    only_c2 = 343 - v12_only - v23_only - v123
    only_c3 = 343 - v13_only - v23_only - v123
    
    v1 = only_c1 + only_c2 + only_c3
    v2 = v12_only + v13_only + v23_only
    v3 = v123
    
    return v1, v2, v3

def solve(target_v1, target_v2, target_v3):
    """
    Try to find cube positions that match the target volumes.
    """
    # Strategy: Try different combinations of cube placements
    # Key observation: we can have cubes overlap by different amounts
    
    # Try offsets from -7 to 7 (enough to cover all useful overlap cases)
    for a1 in range(-7, 8):
        for a2 in range(-7, 8):
            for a3 in range(-7, 8):
                for b1 in range(-7, 8):
                    for b2 in range(-7, 8):
                        for b3 in range(-7, 8):
                            for c1 in range(-7, 8):
                                for c2 in range(-7, 8):
                                    for c3 in range(-7, 8):
                                        cube1 = (a1, b1, c1)
                                        cube2 = (a2, b2, c2)
                                        cube3 = (a3, b3, c3)
                                        
                                        v1, v2, v3 = count_volumes(cube1, cube2, cube3)
                                        if v1 == target_v1 and v2 == target_v2 and v3 == target_v3:
                                            return cube1 + cube2 + cube3
    
    return None

def main():
    line = input().strip()
    parts = line.split()
    v1_target = int(parts[0])
    v2_target = int(parts[1])
    v3_target = int(parts[2])
    
    result = solve(v1_target, v2_target, v3_target)
    
    if result is None:
        print("No")
    else:
        a1, b1, c1, a2, b2, c2, a3, b3, c3 = result
        print("Yes")
        print(a1, b1, c1, a2, b2, c2, a3, b3, c3)

if __name__ == "__main__":
    main()
