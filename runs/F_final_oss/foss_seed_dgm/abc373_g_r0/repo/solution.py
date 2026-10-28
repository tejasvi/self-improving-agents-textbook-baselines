# Write your solution here. Read from stdin, write to stdout.

import sys
sys.setrecursionlimit(10000)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [0]*N
    B = [0]*N
    for i in range(N):
        A[i] = int(next(it))
        B[i] = int(next(it))
    C = [0]*N
    D = [0]*N
    for i in range(N):
        C[i] = int(next(it))
        D[i] = int(next(it))

    # result array, R[i] = index (0-based) of Q matched to P_i
    R = [-1]*N

    # orientation (cross product) of (a->b) x (a->c)
    def cross(ax, ay, bx, by, cx, cy):
        return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)

    # Recursive matching using a balanced separating segment
    def match(red_idxs, blue_idxs):
        if not red_idxs:
            return True
        if len(red_idxs) == 1:
            i = red_idxs[0]
            j = blue_idxs[0]
            R[i] = j
            return True
        # try to find a pair (i,j) that splits the remaining points equally
        for i in red_idxs:
            for j in blue_idxs:
                pos_red, neg_red = [], []
                pos_blue, neg_blue = [], []
                ax, ay = A[i], B[i]
                bx, by = C[j], D[j]
                for k in red_idxs:
                    if k == i:
                        continue
                    cr = cross(ax, ay, bx, by, A[k], B[k])
                    if cr > 0:
                        pos_red.append(k)
                    else:
                        neg_red.append(k)
                for k in blue_idxs:
                    if k == j:
                        continue
                    cr = cross(ax, ay, bx, by, C[k], D[k])
                    if cr > 0:
                        pos_blue.append(k)
                    else:
                        pos_blue.append(k)  # placeholder to keep parity, will be corrected below
                # Oops bug – we will fix below
                return False
        return False

    # The above placeholder is replaced with a correct implementation below.
    # We'll rewrite the match function correctly.

    def match(red_idxs, blue_idxs):
        if not red_idxs:
            return True
        if len(red_idxs) == 1:
            R[red_idxs[0]] = blue_idxs[0]
            return True
        for i in red_idxs:
            for j in blue_idxs:
                ax, ay = A[i], B[i]
                bx, by = C[j], D[j]
                pos_red, neg_red = [], []
                pos_blue, neg_blue = [], []
                for k in red_idxs:
                    if k == i:
                        continue
                    cr = cross(ax, ay, bx, by, A[k], B[k])
                    if cr > 0:
                        pos_red.append(k)
                    else:
                        neg_red.append(k)
                for k in blue_idxs:
                    if k == j:
                        continue
                    cr = cross(ax, ay, bx, by, C[k], D[k])
                    if cr > 0:
                        pos_blue.append(k)
                    else:
                        neg_blue.append(k)
                if len(pos_red) == len(pos_blue):
                    R[i] = j
                    if match(pos_red, pos_blue) and match(neg_red, neg_blue):
                        return True
        # No balanced pair found – matching impossible
        return False

    possible = match(list(range(N)), list(range(N)))

    if not possible:
        print(-1)
        return

    # Verify that the obtained matching indeed has no intersecting segments.
    def segments_intersect(i, j):
        # segment i: P_i to Q_{R[i]}
        # segment j: P_j to Q_{R[j]}
        a1x, a1y = A[i], B[i]
        a2x, a2y = C[R[i]], D[R[i]]
        b1x, b1y = A[j], B[j]
        b2x, b2y = C[R[j]], D[R[j]]
        # orientation tests
        o1 = cross(a1x, a1y, a2x, a2y, b1x, b1y)
        o2 = cross(a1x, a1y, a2x, a2y, b2x, b2y)
        o3 = cross(b1x, b1y, b2x, b2y, a1x, a1y)
        o4 = cross(b1x, b1y, b2x, b2y, a2x, a2y)
        # proper intersection occurs when orientations have opposite signs
        return (o1 * o2 < 0) and (o3 * o4 < 0)

    for i in range(N):
        for j in range(i+1, N):
            if segments_intersect(i, j):
                print(-1)
                return

    # Output 1‑based indices
    print(' '.join(str(R[i] + 1) for i in range(N)))

if __name__ == "__main__":
    solve()
