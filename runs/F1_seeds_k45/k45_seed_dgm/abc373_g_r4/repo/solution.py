# Write your solution here. Read from stdin, write to stdout.

def ccw(A, B, C):
    """Check if three points are in counter-clockwise order"""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(p1, p2, p3, p4):
    """Check if segment p1-p2 and segment p3-p4 intersect (not at endpoints)"""
    # Two segments intersect if their endpoints straddle each other
    # and they are not collinear (already guaranteed by problem)
    
    # Check if they intersect properly (not just touching at endpoints)
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def is_valid_permutation(P, Q, R):
    """Check if permutation R is valid (no segment intersections)"""
    n = len(R)
    segments = [(P[i], Q[R[i] - 1]) for i in range(n)]
    
    # Check all pairs of segments
    for i in range(n):
        for j in range(i + 1, n):
            if segments_intersect(segments[i][0], segments[i][1], segments[j][0], segments[j][1]):
                return False
    return True

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
    # with pruning based on conflict graph
    
    # Build a conflict graph: edge (i, j) means if R[i] = a and R[j] = b (a != b),
    # the segments would intersect
    conflicts = {}
    for i in range(n):
        conflicts[i] = {}
        for q_idx1 in range(n):
            conflicts[i][q_idx1] = set()
            for j in range(n):
                if i >= j:
                    continue
                for q_idx2 in range(n):
                    if q_idx1 == q_idx2:
                        continue
                    if segments_intersect(P[i], Q[q_idx1], P[j], Q[q_idx2]):
                        conflicts[i][q_idx1].add((j, q_idx2))
    
    # Backtracking search
    def backtrack(pos, used, current):
        if pos == n:
            return current[:]
        
        for q_idx in range(n):
            if q_idx in used:
                continue
            
            # Check if this assignment would cause a conflict with already assigned segments
            valid = True
            for prev_pos in range(pos):
                if segments_intersect(P[prev_pos], Q[current[prev_pos] - 1], P[pos], Q[q_idx]):
                    valid = False
                    break
            
            if valid:
                used.add(q_idx)
                current.append(q_idx + 1)
                
                result = backtrack(pos + 1, used, current)
                if result is not None:
                    return result
                
                current.pop()
                used.remove(q_idx)
        
        return None
    
    result = backtrack(0, set(), [])
    
    if result is None:
        print(-1)
    else:
        print(' '.join(map(str, result)))

solve()
