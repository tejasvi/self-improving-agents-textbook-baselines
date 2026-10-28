# Write your solution here. Read from stdin, write to stdout.

import sys
sys.setrecursionlimit(10000)

def orientation(ax, ay, bx, by, cx, cy):
    # cross product (b-a) x (c-a)
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = []  # (x, y, idx)
    for i in range(N):
        x = int(next(it)); y = int(next(it))
        P.append((x, y, i))
    Q = []
    for i in range(N):
        x = int(next(it)); y = int(next(it))
        Q.append((x, y, i))
    R = [-1] * N  # result mapping from P idx to Q idx (0‑based)

    def recurse(Plist, Qlist):
        if not Plist:
            return
        # pick first point from Plist
        px, py, pi = Plist[0]
        for qx, qy, qi in Qlist:
            leftP, rightP = [], []
            leftQ, rightQ = [], []
            # classify remaining P points
            for ox, oy, oi in Plist[1:]:
                if orientation(px, py, qx, qy, ox, oy) > 0:
                    leftP.append((ox, oy, oi))
                else:
                    rightP.append((ox, oy, oi))
            # classify remaining Q points (excluding current q)
            for ox, oy, oi in Qlist:
                if oi == qi:
                    continue
                if orientation(px, py, qx, qy, ox, oy) > 0:
                    leftQ.append((ox, oy, oi))
                else:
                    rightQ.append((ox, oy, oi))
            if len(leftP) == len(leftQ):
                # this pair works
                R[pi] = qi
                recurse(leftP, leftQ)
                recurse(rightP, rightQ)
                return
        # If we exit the loop, something went wrong (should not happen with given constraints)
        # To be safe, output -1 and exit
        print(-1)
        sys.exit(0)

    recurse(P, Q)
    # Convert to 1‑based indices for output
    output = [str(r + 1) for r in R]
    print(' '.join(output))

if __name__ == "__main__":
    solve()
