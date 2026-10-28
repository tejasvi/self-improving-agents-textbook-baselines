def ccw(A, B, C):
    """Check counter-clockwise orientation.
    Returns:
        Positive if counter-clockwise
        Negative if clockwise
        0 if collinear
    """
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def segments_intersect(p1, q1, p2, q2):
    """Check if line segment p1-q1 and p2-q2 intersect.
    Returns True if they intersect, False otherwise.
    """
    # Check if segments are on opposite sides of each other
    def on_segment(p, q, r):
        """Check if point q lies on segment pr"""
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    def orientation(p, q, r):
        """Find orientation of ordered triplet (p, q, r)
        Returns:
            0 if collinear
            1 if clockwise
            2 if counterclockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if abs(val) < 1e-10:
            return 0
        return 1 if val > 0 else 2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases (collinear points)
    # p1, q1, p2 collinear and p2 lies on segment p1-q1
    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    # p1, q1, q2 collinear and q2 lies on segment p1-q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    # p2, q2, p1 collinear and p1 lies on segment p2-q2
    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    # p2, q2, q1 collinear and q1 lies on segment p2-q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False


def solve(P, Q):
    """Find a non-crossing matching between P and Q points."""
    N = len(P)
    
    # For efficiency, precompute which Q indices conflict with which
    # A Q index 'j' conflicts with Q index 'k' if P[i]-Q[j] and P[i]-Q[k] 
    # would cross (for different i's)
    
    def is_valid_matching(assignment):
        """Check if the current assignment is valid (no crossings)."""
        # assignment is a list where assignment[i] = j means P[i] is matched with Q[j]
        for i in range(len(assignment)):
            if assignment[i] == -1:
                continue
            for j in range(i + 1, len(assignment)):
                if assignment[j] == -1:
                    continue
                # Check if segment P[i]-Q[assignment[i]] crosses P[j]-Q[assignment[j]]
                if segments_intersect(P[i], Q[assignment[i]], P[j], Q[assignment[j]]):
                    return False
        return True

    def backtrack(idx, assignment, used):
        """Backtrack to find a valid assignment."""
        if idx == N:
            return is_valid_matching(assignment)
        
        for q_idx in range(N):
            if q_idx in used:
                continue
            
            # Try assigning P[idx] to Q[q_idx]
            assignment[idx] = q_idx
            used.add(q_idx)
            
            # Check if current assignment is still valid
            valid = True
            for i in range(idx):
                if segments_intersect(P[i], Q[assignment[i]], P[idx], Q[q_idx]):
                    valid = False
                    break
            
            if valid and backtrack(idx + 1, assignment, used):
                return True
            
            assignment[idx] = -1
            used.remove(q_idx)
        
        return False

    assignment = [-1] * N
    if backtrack(0, assignment, set()):
        # Convert 0-indexed to 1-indexed
        return [x + 1 for x in assignment]
    else:
        return None


def main():
    N = int(input())
    P = []
    for _ in range(N):
        a, b = map(int, input().split())
        P.append((a, b))
    
    Q = []
    for _ in range(N):
        c, d = map(int, input().split())
        Q.append((c, d))
    
    result = solve(P, Q)
    
    if result is None:
        print(-1)
    else:
        print(' '.join(map(str, result)))


if __name__ == "__main__":
    main()
