# Write your solution here. Read from stdin, write to stdout.

def cross_product(o, a, b):
    """Calculate cross product of vectors OA and OB"""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def segments_intersect(p1, q1, p2, q2):
    """
    Check if line segment p1-q1 and p2-q2 intersect.
    Returns True if they intersect (excluding touching at endpoints).
    """
    # Check if segments have a common endpoint
    if p1 == p2 or p1 == q2 or q1 == p2 or q1 == q2:
        return False
    
    # Check if the segments properly intersect
    # Two segments intersect if:
    # - p1 and q1 are on opposite sides of the line p2-q2, AND
    # - p2 and q2 are on opposite sides of the line p1-q1
    
    d1 = sign(cross_product(p2, q2, p1))
    d2 = sign(cross_product(p2, q2, q1))
    d3 = sign(cross_product(p1, q1, p2))
    d4 = sign(cross_product(p1, q1, q2))
    
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    
    return False

def solve():
    N = int(input())
    
    P = []
    for _ in range(N):
        a, b = map(int, input().split())
        P.append((a, b))
    
    Q = []
    for _ in range(N):
        c, d = map(int, input().split())
        Q.append((c, d))
    
    # Try to find a valid permutation using backtracking
    used = [False] * N
    permutation = []
    
    def is_valid_assignment(p_idx, q_idx):
        """Check if assigning P[p_idx] to Q[q_idx] is valid"""
        current_segment = (P[p_idx], Q[q_idx])
        
        # Check against all previously assigned segments
        for prev_p_idx in range(len(permutation)):
            prev_q_idx = permutation[prev_p_idx]
            prev_segment = (P[prev_p_idx], Q[prev_q_idx])
            
            if segments_intersect(current_segment[0], current_segment[1],
                                 prev_segment[0], prev_segment[1]):
                return False
        
        return True
    
    def backtrack(p_idx):
        """Try to assign Q indices to P points"""
        if p_idx == N:
            return True
        
        for q_idx in range(N):
            if not used[q_idx]:
                if is_valid_assignment(p_idx, q_idx):
                    used[q_idx] = True
                    permutation.append(q_idx)
                    
                    if backtrack(p_idx + 1):
                        return True
                    
                    permutation.pop()
                    used[q_idx] = False
        
        return False
    
    if backtrack(0):
        # Convert 0-indexed to 1-indexed
        result = [q_idx + 1 for q_idx in permutation]
        print(' '.join(map(str, result)))
    else:
        print(-1)

solve()
