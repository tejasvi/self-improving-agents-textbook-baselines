import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    d = [int(data[idx + i]) for i in range(n)]
    idx += n
    l1, c1, k1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    l2, c2, k2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])

    INF = k2 + 1  # any value > k2 means infeasible; cap at INF
    # dp[j]: min type-2 sensors used with exactly j type-1 sensors so far
    dp = [INF] * (k1 + 1)
    dp[0] = 0
    top = 0  # max j reachable so far
    for D in d:
        amax = min(k1, (D + l1 - 1) // l1)
        # need[a] for a in 0..amax
        need = []
        for a in range(amax + 1):
            rem = D - a * l1
            b = (rem + l2 - 1) // l2 if rem > 0 else 0
            need.append(b if b <= k2 else INF)
        new_top = min(k1, top + amax)
        new = [INF] * (k1 + 1)
        for a in range(amax + 1):
            nd = need[a]
            if nd >= INF:
                continue
            # new[j] = min(new[j], dp[j-a] + nd) for j in [a, a+top]
            hi = min(top, k1 - a)
            seg = dp[0:hi + 1]
            # cap so that values > k2 stay at INF
            cand = [x + nd for x in seg]
            tgt = new[a:a + hi + 1]
            new[a:a + hi + 1] = [t if t <= c else c for t, c in zip(tgt, cand)]
        for j in range(new_top + 1):
            if new[j] > k2:
                new[j] = INF
        dp = new
        top = new_top

    best = -1
    for j in range(k1 + 1):
        if dp[j] <= k2:
            cost = j * c1 + dp[j] * c2
            if best < 0 or cost < best:
                best = cost
    print(best)


main()
