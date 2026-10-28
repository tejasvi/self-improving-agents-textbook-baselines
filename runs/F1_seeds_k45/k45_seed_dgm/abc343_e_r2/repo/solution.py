def intersection_volume(a1, b1, c1, a2, b2, c2):
    """Calculate intersection volume of two cubes C(a1,b1,c1) and C(a2,b2,c2)."""
    side = 7
    dx = max(0, min(a1 + side, a2 + side) - max(a1, a2))
    dy = max(0, min(b1 + side, b2 + side) - max(b1, b2))
    dz = max(0, min(c1 + side, c2 + side) - max(c1, c2))
    return dx * dy * dz


def calculate_volumes(a1, b1, c1, a2, b2, c2, a3, b3, c3):
    """Calculate V1, V2, V3 for given cube positions."""
    v12 = intersection_volume(a1, b1, c1, a2, b2, c2)
    v13 = intersection_volume(a1, b1, c1, a3, b3, c3)
    v23 = intersection_volume(a2, b2, c2, a3, b3, c3)
    
    # Triple intersection
    a_min = max(a1, a2, a3)
    a_max = min(a1 + 7, a2 + 7, a3 + 7)
    b_min = max(b1, b2, b3)
    b_max = min(b1 + 7, b2 + 7, b3 + 7)
    c_min = max(c1, c2, c3)
    c_max = min(c1 + 7, c2 + 7, c3 + 7)
    
    v123 = max(0, a_max - a_min) * max(0, b_max - b_min) * max(0, c_max - c_min)
    
    # V3 = volume in all three
    V3 = v123
    
    # V2 = volume in exactly two = (v12 - v123) + (v13 - v123) + (v23 - v123)
    V2 = (v12 - v123) + (v13 - v123) + (v23 - v123)
    
    # V1 = volume in exactly one = 3*343 - V2 - 3*V3
    V1 = 3 * 343 - V2 - 3 * V3
    
    return V1, V2, V3


def solve(V1_target, V2_target, V3_target):
    """Find cube positions that match target volumes."""
    
    # Check the constraint: V1 + 2*V2 + 3*V3 = 1029
    if V1_target + 2 * V2_target + 3 * V3_target != 1029:
        return None
    
    # Case 1: All three cubes at same position
    if (V1_target == 0 and V2_target == 0 and V3_target == 343):
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    # Strategy: Try to construct cubes with controlled overlaps
    # Key insight: we can control overlap by shifting in one dimension
    
    # For efficiency, try placements where cubes are mostly aligned
    # but shifted by amounts from 0 to 7 (full to no overlap)
    
    side = 7
    
    # Try different overlap configurations
    # Place cube 1 at origin
    a1, b1, c1 = 0, 0, 0
    
    # Try all possible shifts in range [-7, 7] for each dimension
    # But be smart about it - we want to create specific overlaps
    
    for a2 in range(-7, 8):
        for b2 in range(-7, 8):
            for c2 in range(-7, 8):
                # Skip if this is same as cube 1
                if a2 == 0 and b2 == 0 and c2 == 0:
                    continue
                    
                for a3 in range(-7, 8):
                    for b3 in range(-7, 8):
                        for c3 in range(-7, 8):
                            # Skip if same as cube 1 or 2
                            if (a3 == 0 and b3 == 0 and c3 == 0) or (a3 == a2 and b3 == b2 and c3 == c2):
                                continue
                            
                            V1, V2, V3 = calculate_volumes(a1, b1, c1, a2, b2, c2, a3, b3, c3)
                            if V1 == V1_target and V2 == V2_target and V3 == V3_target:
                                return (a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    return None


def main():
    line = input().strip()
    V1_target, V2_target, V3_target = map(int, line.split())
    
    result = solve(V1_target, V2_target, V3_target)
    
    if result is None:
        print("No")
    else:
        print("Yes")
        print(" ".join(map(str, result)))


if __name__ == "__main__":
    main()
