import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    hs = [int(data[2 + 2 * i]) for i in range(n)]

    # Visible from (0,h): building i visible iff h > max_{j<i} intercept(line P_j P_i).
    # Max intercept over pairs: for each i, the best j is the tangent point from P_i
    # to the upper convex hull of the prefix points.
    hull = []  # indices into xs/hs, upper hull, increasing x
    best_num = None
    best_den = None  # best = best_num / best_den, best_den > 0
    for i in range(n):
        px, py = xs[i], hs[i]
        if hull:
            lo, hi = 0, len(hull) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                a = hull[mid]
                b = hull[mid + 1]
                # improving: slope(b,P) < slope(a,P)
                if (py - hs[b]) * (px - xs[a]) < (py - hs[a]) * (px - xs[b]):
                    lo = mid + 1
                else:
                    hi = mid
            j = hull[lo]
            num = hs[j] * px - py * xs[j]
            den = px - xs[j]
            if best_num is None or num * best_den > best_num * den:
                best_num, best_den = num, den
        # add point to upper hull
        while len(hull) >= 2:
            a = hull[-2]
            b = hull[-1]
            # remove b if it is not a strict right turn a->b->P
            cross = (xs[b] - xs[a]) * (py - hs[a]) - (hs[b] - hs[a]) * (px - xs[a])
            if cross >= 0:
                hull.pop()
            else:
                break
        hull.append(i)

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print("%.15f" % (best_num / best_den))


main()
