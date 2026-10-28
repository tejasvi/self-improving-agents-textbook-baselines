# Write your solution here. Read from stdin, write to stdout.

def orientation(p, q, r):
    """Find orientation of ordered triplet (p, q, r).
    Returns:
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

def segments_intersect(p1, q1, p2, q2):
    """
    Check if line segment p1-q1 intersects with line segment p2-q2.
    They should not touch at endpoints.
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    # General case
    if o1 != o2 and o3 != o4:
        return True
    
    # Special cases (collinear) - but problem says no 3 points are collinear
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True
    
    return False

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
    
    # Precompute which pairs would intersect (conflict graph)
    # conflicts[i][j] = set of Q indices that would create an intersection with P[i] -> Q[j]
    conflicts = [[set() for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(i):
                for m in range(n):
                    if segments_intersect(P[k], Q[m], P[i], Q[j]):
                        conflicts[i][j].add(m)
    
    # Try to find a valid permutation using backtracking with pruning
    result = [0] * n
    used = [False] * n  # track which Q indices are used
    
    def backtrack(i):
        """Try to assign Q indices to P points starting from P[i]"""
        if i == n:
            return True
        
        # Try assigning each unused Q index to P[i]
        for j in range(n):
            if used[j]:
                continue
            
            # Check if this choice conflicts with any previous assignments
            valid = True
            for k in range(i):
                if result[k] in conflicts[i][j]:
                    valid = False
                    break
            
            if valid:
                result[i] = j
                used[j] = True
                
                if backtrack(i + 1):
                    return True
                
                used[j] = False
        
        return False
    
    if backtrack(0):
        # Convert from 0-indexed to 1-indexed
        print(' '.join(str(x + 1) for x in result))
    else:
        print(-1)

solve()
