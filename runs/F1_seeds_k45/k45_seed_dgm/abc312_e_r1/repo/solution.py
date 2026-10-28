def read_input():
    n = int(input())
    cuboids = []
    for _ in range(n):
        coords = list(map(int, input().split()))
        x1, y1, z1, x2, y2, z2 = coords
        # Ensure x1 < x2, y1 < y2, z1 < z2
        cuboids.append({
            'x': (min(x1, x2), max(x1, x2)),
            'y': (min(y1, y2), max(y1, y2)),
            'z': (min(z1, z2), max(z1, z2))
        })
    return n, cuboids


def overlap_1d(range1, range2):
    """Check if two 1D ranges overlap with positive length."""
    a1, a2 = range1
    b1, b2 = range2
    overlap_start = max(a1, b1)
    overlap_end = min(a2, b2)
    return overlap_end > overlap_start


def overlap_1d_length(range1, range2):
    """Get the length of overlap between two 1D ranges."""
    a1, a2 = range1
    b1, b2 = range2
    overlap_start = max(a1, b1)
    overlap_end = min(a2, b2)
    return max(0, overlap_end - overlap_start)


def share_face(cuboid1, cuboid2):
    """Check if two cuboids share a face with positive area."""
    
    # Check if they touch on an x-plane (faces perpendicular to x-axis)
    # One cuboid's x_max equals the other's x_min
    if cuboid1['x'][1] == cuboid2['x'][0] or cuboid1['x'][0] == cuboid2['x'][1]:
        # Check overlap in y and z dimensions
        y_overlap = overlap_1d_length(cuboid1['y'], cuboid2['y'])
        z_overlap = overlap_1d_length(cuboid1['z'], cuboid2['z'])
        if y_overlap > 0 and z_overlap > 0:
            return True
    
    # Check if they touch on a y-plane (faces perpendicular to y-axis)
    if cuboid1['y'][1] == cuboid2['y'][0] or cuboid1['y'][0] == cuboid2['y'][1]:
        # Check overlap in x and z dimensions
        x_overlap = overlap_1d_length(cuboid1['x'], cuboid2['x'])
        z_overlap = overlap_1d_length(cuboid1['z'], cuboid2['z'])
        if x_overlap > 0 and z_overlap > 0:
            return True
    
    # Check if they touch on a z-plane (faces perpendicular to z-axis)
    if cuboid1['z'][1] == cuboid2['z'][0] or cuboid1['z'][0] == cuboid2['z'][1]:
        # Check overlap in x and y dimensions
        x_overlap = overlap_1d_length(cuboid1['x'], cuboid2['x'])
        y_overlap = overlap_1d_length(cuboid1['y'], cuboid2['y'])
        if x_overlap > 0 and y_overlap > 0:
            return True
    
    return False


def main():
    n, cuboids = read_input()
    
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j and share_face(cuboids[i], cuboids[j]):
                count += 1
        print(count)


if __name__ == "__main__":
    main()
