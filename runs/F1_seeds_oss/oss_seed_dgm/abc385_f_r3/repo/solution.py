# Solution for Visible Buildings problem
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    xs = [0] * n
    hs = [0] * n
    for i in range(n):
        xs[i] = int(next(it))
        hs[i] = int(next(it))
    if n <= 1:
        print(-1)
        return
    # Build upper convex hull of points (x, h)
    hull = []  # list of (x, h)
    for x, h in zip(xs, hs):
        # maintain upper hull (non‑increasing slopes)
        while len(hull) >= 2:
            x1, h1 = hull[-2]
            x2, h2 = hull[-1]
            # cross product to check turn direction
            cross = (x2 - x1) * (h - h2) - (h2 - h1) * (x - x2)
            if cross >= 0:
                hull.pop()
            else:
                break
        hull.append((x, h))
    max_crit = -float('inf')
    for i in range(len(hull) - 1):
        x1, h1 = hull[i]
        x2, h2 = hull[i + 1]
        crit = (h1 * x2 - h2 * x1) / (x2 - x1)
        if crit > max_crit:
            max_crit = crit
    # If the maximal critical height is negative, height 0 already sees all buildings
    if max_crit < 0:
        print(-1)
    else:
        # Print with enough precision (absolute/relative error 1e-9)
        print("{:.15f}".format(max_crit))

if __name__ == "__main__":
    solve()
