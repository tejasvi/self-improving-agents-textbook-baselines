# Write your solution here. Read from stdin, write to stdout.
import sys

def orientation(ax, ay, bx, by, cx, cy):
    """Return cross product (B-A) x (C-A). Positive if C is left of AB."""
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def segments_cross(p1, q1, p2, q2):
    """Return True if segments p1-q1 and p2-q2 intersect (excluding endpoints).
    Problem guarantees no three points collinear, so we can use strict sign test.
    """
    o1 = orientation(p1[0], p1[1], q1[0], q1[1], p2[0], p2[1])
    o2 = orientation(p1[0], p1[1], q1[0], q1[1], q2[0], q2[1])
    o3 = orientation(p2[0], p2[1], q2[0], q2[1], p1[0], p1[1])
    o4 = orientation(p2[0], p2[1], q2[0], q2[1], q1[0], q1[1])
    return o1 * o2 < 0 and o3 * o4 < 0

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [(int(next(it)), int(next(it))) for _ in range(N)]
    Q = [(int(next(it)), int(next(it))) for _ in range(N)]

    # Start with any permutation; identity is fine.
    perm = list(range(N))  # perm[i] = index in Q matched to P[i]

    # Iteratively eliminate crossings by swapping the partners of a crossing pair.
    changed = True
    while changed:
        changed = False
        for i in range(N):
            for j in range(i + 1, N):
                if segments_cross(P[i], Q[perm[i]], P[j], Q[perm[j]]):
                    # swapping eliminates this crossing and does not create a new crossing
                    perm[i], perm[j] = perm[j], perm[i]
                    changed = True
                    break
            if changed:
                break

    # Verify that the resulting matching is indeed non‑crossing.
    ok = True
    for i in range(N):
        for j in range(i + 1, N):
            if segments_cross(P[i], Q[perm[i]], P[j], Q[perm[j]]):
                ok = False
                break
        if not ok:
            break

    if not ok:
        print(-1)
    else:
        # Convert to 1‑based indices as required by the problem statement.
        print(' '.join(str(x + 1) for x in perm))

if __name__ == "__main__":
    solve()
