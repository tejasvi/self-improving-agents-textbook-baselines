import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    d = [int(data[idx + i]) for i in range(n)]
    idx += n
    l1, c1, k1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    l2, c2, k2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = float('inf')
    # dp[j] = minimum number of type-2 sensors needed so far, using exactly j type-1 sensors
    dp = [INF] * (k1 + 1)
    dp[0] = 0
    for D in d:
        amax = min(k1, (D + l1 - 1) // l1)
        # need[a] = type-2 sensors required if this section uses a type-1 sensors
        need = []
        for a in range(amax + 1):
            rem = D - a * l1
            need.append((rem + l2 - 1) // l2 if rem > 0 else 0)
        new = [INF] * (k1 + 1)
        for a in range(amax + 1):
            b = need[a]
            # new[j + a] = min(new[j + a], dp[j] + b) for j in 0..k1-a
            m = k1 + 1 - a
            seg = new[a:]
            cand = [v + b for v in dp[:m]]
            new[a:] = map(min, seg, cand)
        dp = new
    best = INF
    for j in range(k1 + 1):
        y = dp[j]
        if y <= k2:
            cost = c1 * j + c2 * y
            if cost < best:
                best = cost
    print(-1 if best == INF else best)


main()
