def ccw(A, B, C):
    """Check if three points are in counter-clockwise order"""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(p1, p2, p3, p4):
    """Check if line segment p1-p2 and p3-p4 intersect"""
    # Two segments intersect if they have different orientations
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def solve():
    n = int(input())
    
    P = []
    for _ in range(n):
        a, b = map(int, input().split())
        P.append((a, b))
    
    Q = []
    for _ in range(n):
        c, d = map(int, input().split())
        Q.append((c, d))
    
    # Try to find a valid permutation using backtracking
    result = [None] * n
    used = [False] * n
    
    def is_valid_assignment(p_idx, q_idx):
        """Check if assigning P[p_idx] to Q[q_idx] creates any conflicts"""
        # Check against all previously assigned segments
        for prev_p_idx in range(p_idx):
            prev_q_idx = result[prev_p_idx]
            if prev_q_idx is not None:
                # Check if segments P[p_idx]-Q[q_idx] and P[prev_p_idx]-Q[prev_q_idx] intersect
                if segments_intersect(P[p_idx], Q[q_idx], P[prev_p_idx], Q[prev_q_idx]):
                    return False
        return True
    
    def backtrack(p_idx):
        """Try to assign P[p_idx] to some Q[q_idx]"""
        if p_idx == n:
            return True
        
        for q_idx in range(n):
            if not used[q_idx] and is_valid_assignment(p_idx, q_idx):
                result[p_idx] = q_idx
                used[q_idx] = True
                
                if backtrack(p_idx + 1):
                    return True
                
                result[p_idx] = None
                used[q_idx] = False
        
        return False
    
    if backtrack(0):
        # Convert to 1-indexed
        print(' '.join(str(r + 1) for r in result))
    else:
        print(-1)

solve()
