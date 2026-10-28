def get_cuboid_faces(x1, y1, z1, x2, y2, z2):
    """
    Get all 6 faces of a cuboid.
    Each face is represented as a tuple: (plane_type, coordinate, interval1, interval2)
    where plane_type is 'xy', 'xz', or 'yz'
    coordinate is the fixed coordinate value
    interval1 and interval2 are the ranges in the other two dimensions
    """
    faces = []
    # XY planes (z fixed)
    faces.append(('xy', 'z', z1, (x1, x2), (y1, y2)))  # bottom face
    faces.append(('xy', 'z', z2, (x1, x2), (y1, y2)))  # top face
    
    # XZ planes (y fixed)
    faces.append(('xz', 'y', y1, (x1, x2), (z1, z2)))  # front face
    faces.append(('xz', 'y', y2, (x1, x2), (z1, z2)))  # back face
    
    # YZ planes (x fixed)
    faces.append(('yz', 'x', x1, (y1, y2), (z1, z2)))  # left face
    faces.append(('yz', 'x', x2, (y1, y2), (z1, z2)))  # right face
    
    return faces


def intervals_overlap(interval1, interval2):
    """
    Check if two intervals overlap with positive length.
    interval1 and interval2 are tuples (start, end)
    """
    start = max(interval1[0], interval2[0])
    end = min(interval1[1], interval2[1])
    return start < end  # positive length overlap


def faces_share_rectangle(face1, face2):
    """
    Check if two faces share a rectangle with positive area.
    """
    plane1, coord_type1, coord1, interval1_a, interval1_b = face1
    plane2, coord_type2, coord2, interval2_a, interval2_b = face2
    
    # Faces must be on the same type of plane
    if plane1 != plane2:
        return False
    
    # The fixed coordinate must be the same
    if coord1 != coord2:
        return False
    
    # Both intervals must overlap with positive length
    return intervals_overlap(interval1_a, interval2_a) and intervals_overlap(interval1_b, interval2_b)


def solve():
    n = int(input())
    cuboids = []
    
    for _ in range(n):
        coords = list(map(int, input().split()))
        x1, y1, z1, x2, y2, z2 = coords
        cuboids.append((x1, y1, z1, x2, y2, z2))
    
    # For each cuboid, count how many other cuboids share a face with it
    results = []
    
    for i in range(n):
        count = 0
        faces_i = get_cuboid_faces(*cuboids[i])
        
        for j in range(n):
            if i == j:
                continue
            
            faces_j = get_cuboid_faces(*cuboids[j])
            
            # Check if any face of cuboid i shares a rectangle with any face of cuboid j
            shares_face = False
            for face_i in faces_i:
                if shares_face:
                    break
                for face_j in faces_j:
                    if faces_share_rectangle(face_i, face_j):
                        shares_face = True
                        break
            
            if shares_face:
                count += 1
        
        results.append(count)
    
    for result in results:
        print(result)


if __name__ == "__main__":
    solve()
