# Write your solution here. Read from stdin, write to stdout.

def read_input():
    n = int(input())
    cuboids = []
    for _ in range(n):
        coords = list(map(int, input().split()))
        x1, y1, z1, x2, y2, z2 = coords
        cuboids.append((x1, y1, z1, x2, y2, z2))
    return n, cuboids

def cuboids_share_face(c1, c2):
    """
    Check if two cuboids share a face with positive area.
    A cuboid is represented as (x1, y1, z1, x2, y2, z2) where x1 < x2, y1 < y2, z1 < z2
    """
    x1_1, y1_1, z1_1, x2_1, y2_1, z2_1 = c1
    x1_2, y1_2, z1_2, x2_2, y2_2, z2_2 = c2
    
    # Check all 6 face pairs (one from each cuboid)
    # We need to check if they touch on a common face
    
    # Check if they touch on a face perpendicular to x-axis
    # c1's right face (x=x2_1) touches c2's left face (x=x1_2)
    if x2_1 == x1_2:
        # Check if y ranges overlap
        y_overlap_min = max(y1_1, y1_2)
        y_overlap_max = min(y2_1, y2_2)
        # Check if z ranges overlap
        z_overlap_min = max(z1_1, z1_2)
        z_overlap_max = min(z2_1, z2_2)
        
        if y_overlap_min < y_overlap_max and z_overlap_min < z_overlap_max:
            return True
    
    # c1's left face (x=x1_1) touches c2's right face (x=x2_2)
    if x1_1 == x2_2:
        # Check if y ranges overlap
        y_overlap_min = max(y1_1, y1_2)
        y_overlap_max = min(y2_1, y2_2)
        # Check if z ranges overlap
        z_overlap_min = max(z1_1, z1_2)
        z_overlap_max = min(z2_1, z2_2)
        
        if y_overlap_min < y_overlap_max and z_overlap_min < z_overlap_max:
            return True
    
    # Check if they touch on a face perpendicular to y-axis
    # c1's front face (y=y2_1) touches c2's back face (y=y1_2)
    if y2_1 == y1_2:
        # Check if x ranges overlap
        x_overlap_min = max(x1_1, x1_2)
        x_overlap_max = min(x2_1, x2_2)
        # Check if z ranges overlap
        z_overlap_min = max(z1_1, z1_2)
        z_overlap_max = min(z2_1, z2_2)
        
        if x_overlap_min < x_overlap_max and z_overlap_min < z_overlap_max:
            return True
    
    # c1's back face (y=y1_1) touches c2's front face (y=y2_2)
    if y1_1 == y2_2:
        # Check if x ranges overlap
        x_overlap_min = max(x1_1, x1_2)
        x_overlap_max = min(x2_1, x2_2)
        # Check if z ranges overlap
        z_overlap_min = max(z1_1, z1_2)
        z_overlap_max = min(z2_1, z2_2)
        
        if x_overlap_min < x_overlap_max and z_overlap_min < z_overlap_max:
            return True
    
    # Check if they touch on a face perpendicular to z-axis
    # c1's top face (z=z2_1) touches c2's bottom face (z=z1_2)
    if z2_1 == z1_2:
        # Check if x ranges overlap
        x_overlap_min = max(x1_1, x1_2)
        x_overlap_max = min(x2_1, x2_2)
        # Check if y ranges overlap
        y_overlap_min = max(y1_1, y1_2)
        y_overlap_max = min(y2_1, y2_2)
        
        if x_overlap_min < x_overlap_max and y_overlap_min < y_overlap_max:
            return True
    
    # c1's bottom face (z=z1_1) touches c2's top face (z=z2_2)
    if z1_1 == z2_2:
        # Check if x ranges overlap
        x_overlap_min = max(x1_1, x1_2)
        x_overlap_max = min(x2_1, x2_2)
        # Check if y ranges overlap
        y_overlap_min = max(y1_1, y1_2)
        y_overlap_max = min(y2_1, y2_2)
        
        if x_overlap_min < x_overlap_max and y_overlap_min < y_overlap_max:
            return True
    
    return False

def main():
    n, cuboids = read_input()
    
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j:
                if cuboids_share_face(cuboids[i], cuboids[j]):
                    count += 1
        print(count)

if __name__ == "__main__":
    main()
