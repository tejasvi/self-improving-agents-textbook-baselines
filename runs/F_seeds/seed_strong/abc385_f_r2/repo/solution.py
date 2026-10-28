import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = [int(data[1 + 2 * k]) for k in range(n)]
    H = [int(data[2 + 2 * k]) for k in range(n)]
    # Max over pairs j<i of intercept at x=0 of line through j and i.
    # For fixed i, best j minimizes slope(j,i): tangent from i to upper hull of prefix.
    best_num = None
    best_den = 1
    hull = []  # indices, upper hull of prefix, increasing X
    for i in range(n):
        xi = X[i]
        yi = H[i]
        L = len(hull)
        if L >= 1:
            lo, hi = 0, L - 1
            while lo < hi:
                mid = (lo + hi) >> 1
                a = hull[mid]
                b = hull[mid + 1]
                # slope(b,i) < slope(a,i) ?
                if (yi - H[b]) * (xi - X[a]) < (yi - H[a]) * (xi - X[b]):
                    lo = mid + 1
                else:
                    hi = mid
            j = hull[lo]
            num = H[j] * xi - yi * X[j]
            den = xi - X[j]
            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den
        # push i into upper hull
        while len(hull) >= 2:
            a = hull[-2]
            b = hull[-1]
            cross = (X[b] - X[a]) * (yi - H[a]) - (H[b] - H[a]) * (xi - X[a])
            if cross >= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    if best_num is None or best_num < 0:
        print(-1)
        return
    # exact rational to decimal
    ip = best_num // best_den
    rem = best_num - ip * best_den
    frac = rem * 10**18 // best_den
    print(f"{ip}.{frac:018d}")


main()
