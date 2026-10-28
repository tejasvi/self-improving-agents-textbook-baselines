import sys
from itertools import accumulate


def values_in_range(coords, D):
    """Return list of S(t) = sum |t - c| for t in [min-D, max+D], restricted to values <= D."""
    n = len(coords)
    lo = min(coords) - D
    hi = max(coords) + D
    size = hi - lo + 1
    cnt = [0] * size
    for c in coords:
        cnt[c - lo] += 1
    le = list(accumulate(cnt))  # le[k] = #coords <= lo + k
    f0 = sum(abs(lo - c) for c in coords)
    # step from lo+k to lo+k+1 changes value by #(<=) - #(>) = 2*le[k] - n
    steps = [f0]
    steps.extend(2 * l - n for l in le[:-1])
    vals = accumulate(steps)
    return [v for v in vals if v <= D]


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    D = int(data[1])
    xs = data[2:2 + 2 * n:2]
    ys = data[3:3 + 2 * n:2]
    xs = [int(v) for v in xs]
    ys = [int(v) for v in ys]

    fv = values_in_range(xs, D)
    gv = values_in_range(ys, D)

    hist = [0] * (D + 1)
    for g in gv:
        hist[g] += 1
    pref = list(accumulate(hist))
    ans = 0
    for f in fv:
        ans += pref[D - f]
    print(ans)


main()
