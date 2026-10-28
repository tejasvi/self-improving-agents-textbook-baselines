# Write your solution here. Read from stdin, write to stdout.
import sys

def orientation(ax, ay, bx, by, cx, cy):
    # cross product (b-a) x (c-a)
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def segments_intersect(p1, p2, p3, p4):
    # each point is (x,y). No three points are collinear.
    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3
    (x4, y4) = p4
    o1 = orientation(x1, y1, x2, y2, x3, y3)
    o2 = orientation(x1, y1, x2, y2, x4, y4)
    o3 = orientation(x3, y3, x4, y4, x1, y1)
    o4 = orientation(x3, y3, x4, y4, x2, y2)
    return o1 * o2 < 0 and o3 * o4 < 0

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = []
    for _ in range(N):
        A = int(next(it)); B = int(next(it))
        P.append((A, B))
    Q = []
    for _ in range(N):
        C = int(next(it)); D = int(next(it))
        Q.append((C, D))
    # start with identity matching (0-indexed)
    R = list(range(N))
    # Resolve crossings by swapping ends until none remain
    while True:
        found = False
        for i in range(N):
            for j in range(i + 1, N):
                if segments_intersect(P[i], Q[R[i]], P[j], Q[R[j]]):
                    R[i], R[j] = R[j], R[i]
                    found = True
                    break
            if found:
                break
        if not found:
            break
    # Output 1-indexed permutation
    print(' '.join(str(r + 1) for r in R))

if __name__ == "__main__":
    solve()
