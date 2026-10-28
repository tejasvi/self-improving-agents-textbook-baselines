# Solution for "No Cross Matching"
# Implements recursive construction of a non‑crossing perfect matching between two point sets.
# The algorithm finds a pair (P_i, Q_j) such that the line segment divides the remaining points
# into equal numbers of P's and Q's on each side, then recurses on both sides.
# If no such pair exists (which should not happen under the given constraints), we output -1.

import sys
sys.setrecursionlimit(10000)

def orient(a, b, c):
    """Return cross product (b-a) x (c-a). Positive if c is to the left of a->b."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [(int(next(it)), int(next(it))) for _ in range(N)]
    Q = [(int(next(it)), int(next(it))) for _ in range(N)]
    R = [-1] * N  # answer: for each P_i, index of Q matched (0‑based)

    # Recursive function working with lists of remaining indices
    def build(p_idxs, q_idxs):
        if not p_idxs:
            return True
        # try every possible pair until we find a balanced split
        for i in p_idxs:
            for j in q_idxs:
                left_p = []
                left_q = []
                # classify remaining P points w.r.t line Pi‑Qj
                for pi in p_idxs:
                    if pi == i:
                        continue
                    sign = orient(P[i], Q[j], P[pi])
                    if sign > 0:
                        left_p.append(pi)
                # classify remaining Q points
                for qj in q_idxs:
                    if qj == j:
                        continue
                    sign = orient(P[i], Q[j], Q[qj])
                    if sign > 0:
                        left_q.append(qj)
                if len(left_p) == len(left_q):
                    # found a suitable pair
                    R[i] = j
                    # build right side lists (sign < 0)
                    right_p = [pi for pi in p_idxs if pi != i and orient(P[i], Q[j], P[pi]) < 0]
                    right_q = [qj for qj in q_idxs if qj != j and orient(P[i], Q[j], Q[qj]) < 0]
                    # recurse on both sides
                    ok_left = build(left_p, left_q)
                    ok_right = build(right_p, right_q)
                    return ok_left and ok_right
        # If we exit the loops, no balanced pair was found – should not happen.
        return False

    possible = build(list(range(N)), list(range(N)))
    if not possible:
        print(-1)
    else:
        # convert to 1‑based indices
        print(' '.join(str(R[i] + 1) for i in range(N)))

if __name__ == "__main__":
    solve()
