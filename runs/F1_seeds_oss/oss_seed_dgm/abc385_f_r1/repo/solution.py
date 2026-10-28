# Visible Buildings solution
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    X = []
    H = []
    for _ in range(n):
        X.append(int(next(it)))
        H.append(int(next(it)))
    if n <= 1:
        print(-1)
        return
    # Build upper convex hull (keeping points with decreasing slopes)
    hull_idx = []  # store indices of points in hull
    for i in range(n):
        # while last two points and new point makes the middle point non-convex, pop
        while len(hull_idx) >= 2:
            i1 = hull_idx[-2]
            i2 = hull_idx[-1]
            # slope(i1,i2) and slope(i2,i)
            # For upper hull we need slope(i1,i2) > slope(i2,i)
            # i.e., (H[i2]-H[i1])/(X[i2]-X[i1]) > (H[i]-H[i2])/(X[i]-X[i2])
            # Cross-multiply to avoid division:
            left = (H[i2] - H[i1]) * (X[i] - X[i2])
            right = (H[i] - H[i2]) * (X[i2] - X[i1])
            if left <= right:  # not strictly decreasing, pop i2
                hull_idx.pop()
            else:
                break
        hull_idx.append(i)
    max_bound = -1e30
    for k in range(len(hull_idx) - 1):
        i = hull_idx[k]
        j = hull_idx[k + 1]
        # Compute bound = (H_i*X_j - H_j*X_i) / (X_j - X_i)
        num = H[i] * X[j] - H[j] * X[i]
        den = X[j] - X[i]
        bound = num / den
        if bound > max_bound:
            max_bound = bound
    # If the maximum bound is negative, answer is -1 (all visible even at height 0)
    if max_bound < 0:
        print(-1)
    else:
        # Print with enough precision
        print("{:.15f}".format(max_bound))

if __name__ == "__main__":
    solve()
