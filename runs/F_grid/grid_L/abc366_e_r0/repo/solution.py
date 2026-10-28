import sys


def values_in_range(vs, D):
    """Yield f(t) = sum |t - v| for t in [vs[0]-D, vs[0]+D] (sorted vs)."""
    n = len(vs)
    L = vs[0] - D
    R = vs[0] + D
    f = 0
    for v in vs:
        f += v - L
    p = 0
    while p < n and vs[p] <= L:
        p += 1
    out = []
    t = L
    while True:
        out.append(f)
        if t == R:
            break
        # f(t+1) - f(t) = #(v <= t) - #(v > t) = 2*p - n
        f += 2 * p - n
        t += 1
        while p < n and vs[p] <= t:
            p += 1
    return out


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    D = int(data[1])
    xs = []
    ys = []
    for i in range(n):
        xs.append(int(data[2 + 2 * i]))
        ys.append(int(data[3 + 2 * i]))
    xs.sort()
    ys.sort()
    fx = values_in_range(xs, D)
    gy = values_in_range(ys, D)

    cnt = [0] * (D + 1)
    for g in gy:
        if g <= D:
            cnt[g] += 1
    # prefix[k] = number of y with g(y) <= k
    acc = 0
    for k in range(D + 1):
        acc += cnt[k]
        cnt[k] = acc
    pre = cnt

    ans = 0
    for f in fx:
        if f <= D:
            ans += pre[D - f]
    print(ans)


main()
