def ccw(A, B, C):
    """
    Check the counter-clockwise orientation of three points.
    Returns:
        1 if counter-clockwise
        -1 if clockwise
        0 if collinear
    """
    val = (C[1] - A[1]) * (B[0] - A[0]) - (B[1] - A[1]) * (C[0] - A[0])
    if val == 0:
        return 0
    return 1 if val > 0 else -1


def segments_intersect(p1, p2, p3, p4):
    """
    Check if line segment p1-p2 and p3-p4 intersect.
    """
    o1 = ccw(p1, p2, p3)
    o2 = ccw(p1, p2, p4)
    o3 = ccw(p3, p4, p1)
    o4 = ccw(p3, p4, p2)
    
    # General case: segments intersect if orientations are different
    if o1 != o2 and o3 != o4:
        return True
    
    # The problem states no three points are collinear, so we don't need
    # to handle the collinear cases
    return False


def solve():
    n = int(input())
    P = []
    Q = []
    
    for _ in range(n):
        a, b = map(int, input().split())
        P.append((a, b))
    
    for _ in range(n):
        c, d = map(int, input().split())
        Q.append((c, d))
    
    # Try to find a valid permutation using backtracking
    used = [False] * n
    result = []
    
    def backtrack(idx):
        if idx == n:
            return True
        
        for q_idx in range(n):
            if used[q_idx]:
                continue
            
            # Check if connecting P[idx] to Q[q_idx] causes any intersection
            valid = True
            segment_p = P[idx]
            segment_q = Q[q_idx]
            
            # Check against all previously added segments
            for i in range(idx):
                prev_p = P[i]
                prev_q = Q[result[i]]
                
                if segments_intersect(segment_p, segment_q, prev_p, prev_q):
                    valid = False
                    break
            
            if valid:
                used[q_idx] = True
                result.append(q_idx)
                
                if backtrack(idx + 1):
                    return True
                
                result.pop()
                used[q_idx] = False
        
        return False
    
    if backtrack(0):
        # Convert to 1-indexed and print
        print(' '.join(str(x + 1) for x in result))
    else:
        print(-1)


solve()
