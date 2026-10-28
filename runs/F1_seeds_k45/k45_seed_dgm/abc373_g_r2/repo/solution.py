def ccw(A, B, C):
    """Check if three points are in counter-clockwise order"""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(p1, p2, p3, p4):
    """Check if line segment p1-p2 intersects with line segment p3-p4"""
    # Two segments intersect if the endpoints of each segment are on opposite sides
    # of the other segment
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def can_add_edge(p_idx, q_idx, P, Q, current_assignment):
    """
    Check if we can add edge from P[p_idx] to Q[q_idx]
    given the current partial assignment
    """
    p_point = P[p_idx]
    q_point = Q[q_idx]
    
    # Check against all already assigned edges
    for pi, qi in enumerate(current_assignment):
        if qi is not None:  # This P point already has an assignment
            # Check if the new segment intersects with this existing segment
            if segments_intersect(p_point, q_point, P[pi], Q[qi]):
                return False
    
    return True

def solve_backtrack(P, Q, N, current_assignment, used_q):
    """
    Backtracking solution to find a valid permutation
    """
    # Find the next P point to assign
    p_idx = -1
    for i in range(N):
        if current_assignment[i] is None:
            p_idx = i
            break
    
    # Base case: all P points have been assigned
    if p_idx == -1:
        return True
    
    # Try assigning each available Q point to this P point
    for q_idx in range(N):
        if not used_q[q_idx]:
            # Check if this assignment is valid
            if can_add_edge(p_idx, q_idx, P, Q, current_assignment):
                # Make the assignment
                current_assignment[p_idx] = q_idx
                used_q[q_idx] = True
                
                # Recursively try to solve the rest
                if solve_backtrack(P, Q, N, current_assignment, used_q):
                    return True
                
                # Backtrack
                current_assignment[p_idx] = None
                used_q[q_idx] = False
    
    return False

def main():
    N = int(input())
    P = []
    Q = []
    
    for _ in range(N):
        a, b = map(int, input().split())
        P.append((a, b))
    
    for _ in range(N):
        c, d = map(int, input().split())
        Q.append((c, d))
    
    current_assignment = [None] * N
    used_q = [False] * N
    
    if solve_backtrack(P, Q, N, current_assignment, used_q):
        # Convert to 1-indexed
        result = [q + 1 for q in current_assignment]
        print(' '.join(map(str, result)))
    else:
        print(-1)

if __name__ == '__main__':
    main()
