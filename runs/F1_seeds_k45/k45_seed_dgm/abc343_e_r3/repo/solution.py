#!/usr/bin/env python3

def get_cube_volume(a1, b1, c1, a2, b2, c2, a3, b3, c3):
    """Calculate the volume contained in exactly 1, 2, 3 cubes."""
    # Create a list of all cubes
    cubes = [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)]
    
    # We need to compute volumes precisely using inclusion-exclusion
    # For a more robust approach, we can sample points or use analytical computation
    
    # Let's use a finer granularity sampling approach for verification
    # Since coordinates can be large, we need to be smart about this
    
    # Better approach: compute intersection volumes analytically
    # For two cubes C(a1,b1,c1) and C(a2,b2,c2):
    # Intersection volume = overlap_x * overlap_y * overlap_z
    # where overlap_x = max(0, min(a1+7, a2+7) - max(a1, a2))
    
    def intersection_volume(cubes_subset):
        """Calculate intersection volume of a subset of cubes."""
        if not cubes_subset:
            return 0
        
        # For each dimension, find the intersection
        min_x = max(c[0] for c in cubes_subset)
        max_x = min(c[0] + 7 for c in cubes_subset)
        min_y = max(c[1] for c in cubes_subset)
        max_y = min(c[1] + 7 for c in cubes_subset)
        min_z = max(c[2] for c in cubes_subset)
        max_z = min(c[2] + 7 for c in cubes_subset)
        
        vol_x = max(0, max_x - min_x)
        vol_y = max(0, max_y - min_y)
        vol_z = max(0, max_z - min_z)
        
        return vol_x * vol_y * vol_z
    
    # Single cube volumes
    v1 = intersection_volume([cubes[0]])
    v2 = intersection_volume([cubes[1]])
    v3 = intersection_volume([cubes[2]])
    
    # Pairwise intersections
    v12 = intersection_volume([cubes[0], cubes[1]])
    v13 = intersection_volume([cubes[0], cubes[2]])
    v23 = intersection_volume([cubes[1], cubes[2]])
    
    # Triple intersection
    v123 = intersection_volume([cubes[0], cubes[1], cubes[2]])
    
    # Volume in exactly one cube (using inclusion-exclusion)
    # = (v1 + v2 + v3) - 2*(v12 + v13 + v23) + 3*v123
    v_exactly_one = v1 + v2 + v3 - 2*(v12 + v13 + v23) + 3*v123
    
    # Volume in exactly two cubes
    # = (v12 + v13 + v23) - 3*v123
    v_exactly_two = v12 + v13 + v23 - 3*v123
    
    # Volume in all three cubes
    v_all_three = v123
    
    return v_exactly_one, v_exactly_two, v_all_three


def solve(V1, V2, V3):
    """Find cube positions that satisfy the volume constraints."""
    
    # Basic constraint check
    max_total = 3 * 343  # 1029
    if V1 + V2 + V3 > max_total:
        return None
    
    # Try various configurations
    # Strategy: parameterize by overlap in each dimension
    
    # Key insight: if we have overlaps d1, d2, d3 (in each dimension) between two cubes,
    # the intersection is d1*d2*d3.
    
    # Simple configuration: position cubes with specific overlaps
    
    # Configuration 1: Three cubes arranged in a line with partial overlaps
    # C1 at (0,0,0), C2 at (d, 0, 0), C3 at (0, d, 0)
    # This creates overlap between C1-C2 of d³, between C1-C3 of d³, between C2-C3 of 0
    
    for d in range(8):  # Overlap distances from 0 to 7
        for d2 in range(8):  # For a different configuration
            # Try configuration: C1 at origin, C2 overlaps by d in x, C3 overlaps by d in y
            a1, b1, c1 = 0, 0, 0
            a2, b2, c2 = d, 0, 0
            a3, b3, c3 = 0, d2, 0
            
            v1, v2, v3 = get_cube_volume(a1, b1, c1, a2, b2, c2, a3, b3, c3)
            if v1 == V1 and v2 == V2 and v3 == V3:
                return (a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    # Configuration 2: Try with overlaps in multiple dimensions
    for d in range(8):
        for d2 in range(8):
            for d3 in range(8):
                # C1 at origin, C2 overlaps by d in x, C3 overlaps by d2 in y and d3 in z
                a1, b1, c1 = 0, 0, 0
                a2, b2, c2 = d, 0, 0
                a3, b3, c3 = 0, d2, d3
                
                v1, v2, v3 = get_cube_volume(a1, b1, c1, a2, b2, c2, a3, b3, c3)
                if v1 == V1 and v2 == V2 and v3 == V3:
                    return (a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    # Configuration 3: All three with partial overlaps
    for d12 in range(8):
        for d13 in range(8):
            for d23 in range(8):
                # C1 at origin
                # C2 overlaps C1 by d12 in x direction
                # C3 overlaps C1 by d13 in y direction and C2 by d23 in z
                a1, b1, c1 = 0, 0, 0
                a2, b2, c2 = d12, 0, 0
                a3, b3, c3 = 0, d13, d23
                
                v1, v2, v3 = get_cube_volume(a1, b1, c1, a2, b2, c2, a3, b3, c3)
                if v1 == V1 and v2 == V2 and v3 == V3:
                    return (a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    # More comprehensive search with different offsets in all dimensions
    for offset in range(-7, 8):
        for offset2 in range(-7, 8):
            for offset3 in range(-7, 8):
                a1, b1, c1 = 0, 0, 0
                a2, b2, c2 = offset, 0, 0
                a3, b3, c3 = 0, offset2, offset3
                
                v1, v2, v3 = get_cube_volume(a1, b1, c1, a2, b2, c2, a3, b3, c3)
                if v1 == V1 and v2 == V2 and v3 == V3:
                    return (a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    # Try with all three cubes having different centers
    for o1 in range(-7, 8):
        for o2 in range(-7, 8):
            for o3 in range(-7, 8):
                a1, b1, c1 = 0, 0, 0
                a2, b2, c2 = o1, o1, 0
                a3, b3, c3 = o2, 0, o3
                
                v1, v2, v3 = get_cube_volume(a1, b1, c1, a2, b2, c2, a3, b3, c3)
                if v1 == V1 and v2 == V2 and v3 == V3:
                    return (a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    return None


def main():
    line = input().strip()
    V1, V2, V3 = map(int, line.split())
    
    result = solve(V1, V2, V3)
    
    if result:
        print("Yes")
        print(*result)
    else:
        print("No")


if __name__ == "__main__":
    main()
