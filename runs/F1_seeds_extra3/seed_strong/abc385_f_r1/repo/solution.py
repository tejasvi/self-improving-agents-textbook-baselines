import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1:2 * n + 1:2]]
    hs = [int(v) for v in data[2:2 * n + 2:2]]
    # Intercept at x=0 of line through j<i is (H_j*X_i - H_i*X_j)/(X_i - X_j).
    # For fixed i, maximize it = minimize slope(j,i) over j<i, found by a
    # tangent binary search on the upper hull of the prefix.
    hx = []
    hh = []
    best_n = None
    best_d = 1
    for i in range(n):
        xi = xs[i]
        hi_ = hs[i]
        m = len(hx)
        if m:
            lo, hi = 0, m - 1
            while lo < hi:
                mid = (lo + hi) >> 1
                xa, ha = hx[mid], hh[mid]
                xb, hb = hx[mid + 1], hh[mid + 1]
                # slope(a,i) > slope(b,i) ?
                if (hi_ - ha) * (xi - xb) > (hi_ - hb) * (xi - xa):
                    lo = mid + 1
                else:
                    hi = mid
            xj, hj = hx[lo], hh[lo]
            num = hj * xi - hi_ * xj
            den = xi - xj
            if best_n is None or num * best_d > best_n * den:
                best_n, best_d = num, den
        # maintain upper hull of prefix
        while len(hx) >= 2:
            x1, h1 = hx[-2], hh[-2]
            x2, h2 = hx[-1], hh[-1]
            if (h2 - h1) * (xi - x1) <= (hi_ - h1) * (x2 - x1):
                hx.pop()
                hh.pop()
            else:
                break
        hx.append(xi)
        hh.append(hi_)
    if best_n is None or best_n < 0:
        print(-1)
    else:
        print("%.18f" % (best_n / best_d))


main()
