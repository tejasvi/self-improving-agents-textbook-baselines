def ccw(A, B, C):
    """Check if three points are in counter-clockwise order."""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(A, B, C, D):
    """Check if segment AB and segment CD intersect (not including endpoints)."""
    # Two segments intersect if:
    # - A and B are on opposite sides of line CD, AND
    # - C and D are on opposite sides of line AB
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def solve():
    N = int(input())
    P = []
    Q = []
    
    for i in range(N):
        a, b = map(int, input().split())
        P.append((a, b))
    
    for i in range(N):
        c, d = map(int, input().split())
        Q.append((c, d))
    
    # Try to find a valid permutation using backtracking
    result = [-1] * N
    used = [False] * N
    
    def can_add_segment(p_idx, q_idx, current_segments):
        """Check if we can add segment from P[p_idx] to Q[q_idx]."""
        p = P[p_idx]
        q = Q[q_idx]
        
        for prev_p_idx, prev_q_idx in current_segments:
            prev_p = P[prev_p_idx]
            prev_q = Q[prev_q_idx]
            if segments_intersect(p, q, prev_p, prev_q):
                return False
        return True
    
    def backtrack(pos, current_segments):
        """Try to build a valid permutation using backtracking."""
        if pos == N:
            return True
        
        # Try to match P[pos] with each unused Q
        for q_idx in range(N):
            if not used[q_idx]:
                if can_add_segment(pos, q_idx, current_segments):
                    result[pos] = q_idx + 1
                    used[q_idx] = True
                    current_segments.append((pos, q_idx))
                    
                    if backtrack(pos + 1, current_segments):
                        return True
                    
                    current_segments.pop()
                    used[q_idx] = False
                    result[pos] = -1
        
        return False
    
    if backtrack(0, []):
        print(' '.join(map(str, result)))
    else:
        print(-1)

solve()
