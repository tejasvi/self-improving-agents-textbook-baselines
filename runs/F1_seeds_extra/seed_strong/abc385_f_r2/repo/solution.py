import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    hs = [int(data[2 + 2 * i]) for i in range(n)]

    # Answer = max over pairs j<i of y-intercept (at x=0) of line through (X_j,H_j),(X_i,H_i).
    # For each i, the best j is the tangent point on the upper hull of previous points.
    hull = []  # indices of upper convex hull of prefix (x increasing)
    best_num = None
    best_den = 1
    for i in range(n):
        xi = xs[i]
        hi_ = hs[i]
        k = len(hull)
        if k > 0:
            # find j minimizing slope(j, i) over hull vertices
            lo, hi = 0, k - 1
            while lo < hi:
                mid = (lo + hi) // 2
                a = hull[mid]
                b = hull[mid + 1]
                # slope(b,i) < slope(a,i) ?
                if (hi_ - hs[b]) * (xi - xs[a]) < (hi_ - hs[a]) * (xi - xs[b]):
                    lo = mid + 1
                else:
                    hi = mid
            j = hull[lo]
            num = hs[j] * xi - hi_ * xs[j]
            den = xi - xs[j]
            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den
        # add point i to upper hull
        while len(hull) >= 2:
            a = hull[-2]
            b = hull[-1]
            # cross(b-a, i-a) >= 0 means b is not strictly above segment a-i
            cr = (xs[b] - xs[a]) * (hi_ - hs[a]) - (hs[b] - hs[a]) * (xi - xs[a])
            if cr >= 0:
                hull.pop()
            else:
                break
        hull.append(i)

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print("%.18f" % (best_num / best_den))


main()
