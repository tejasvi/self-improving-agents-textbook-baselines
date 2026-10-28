# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    V1, V2, V3 = map(int, data)
    SIDE = 7
    CUBE_VOLUME = SIDE ** 3  # 343
    TOTAL_SINGLE = 3 * CUBE_VOLUME  # sum of volumes of three cubes
    # Necessary condition derived from inclusion-exclusion
    if V1 != TOTAL_SINGLE - 2 * V2 - 3 * V3:
        print("No")
        return
    # Additional obvious bounds
    if V3 < 0 or V3 > CUBE_VOLUME:
        print("No")
        return
    if V2 < 0 or V2 > 3 * CUBE_VOLUME:
        print("No")
        return
    # The sum of pairwise intersections must be feasible
    required_pair_sum = V2 + 3 * V3  # equals sum of volumes of three pairwise intersections
    # Enumerate offsets for the second and third cubes relative to the first cube placed at (0,0,0)
    range_vals = range(-SIDE, SIDE + 1)  # -7 .. 7 inclusive
    for dx2 in range_vals:
        len12x = SIDE - abs(dx2)
        for dy2 in range_vals:
            len12y = SIDE - abs(dy2)
            for dz2 in range_vals:
                len12z = SIDE - abs(dz2)
                p12 = len12x * len12y * len12z  # volume of intersection C1 ∩ C2
                for dx3 in range_vals:
                    len13x = SIDE - abs(dx3)
                    for dy3 in range_vals:
                        len13y = SIDE - abs(dy3)
                        for dz3 in range_vals:
                            len13z = SIDE - abs(dz3)
                            p13 = len13x * len13y * len13z  # volume of intersection C1 ∩ C3
                            # Triple overlap lengths along each axis
                            t_x = max(0, min(SIDE, dx2 + SIDE, dx3 + SIDE) - max(0, dx2, dx3))
                            t_y = max(0, min(SIDE, dy2 + SIDE, dy3 + SIDE) - max(0, dy2, dy3))
                            t_z = max(0, min(SIDE, dz2 + SIDE, dz3 + SIDE) - max(0, dz2, dz3))
                            if t_x * t_y * t_z != V3:
                                continue
                            # Intersection between cube2 and cube3
                            ddx = dx3 - dx2
                            ddy = dy3 - dy2
                            ddz = dz3 - dz2
                            len23x = max(0, SIDE - abs(ddx))
                            len23y = max(0, SIDE - abs(ddy))
                            len23z = max(0, SIDE - abs(ddz))
                            p23 = len23x * len23y * len23z
                            if p12 + p13 + p23 == required_pair_sum:
                                print("Yes")
                                # coordinates are within [-100, 100] as required
                                print(f"0 0 0 {dx2} {dy2} {dz2} {dx3} {dy3} {dz3}")
                                return
    print("No")

if __name__ == "__main__":
    solve()
