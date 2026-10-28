import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = K2 + 1  # any value > K2 means infeasible
    # dp[j] = min number of type-2 sensors so that exactly j type-1 sensors
    # are used over the sections processed so far (capped at INF).
    dp = [INF] * (K1 + 1)
    dp[0] = 0
    for d in D:
        # need(a) = type-2 sensors needed if a type-1 sensors cover this section
        m = min(K1, -(-d // L1))
        needs = []
        for a in range(m + 1):
            rem = d - a * L1
            nd = 0 if rem <= 0 else -(-rem // L2)
            needs.append(min(nd, INF))
        new = [INF] * (K1 + 1)
        for a in range(m + 1):
            c = needs[a]
            if c > K2:
                continue
            # candidate for new[j + a] = dp[j] + c, for j in 0..K1-a
            cand = [x + c for x in dp[: K1 + 1 - a]]
            seg = new[a:]
            new[a:] = map(min, seg, cand)
        # cap values
        dp = [x if x <= K2 else INF for x in new]

    best = None
    for j in range(K1 + 1):
        t2 = dp[j]
        if t2 <= K2:
            # type-1 count j, type-2 count t2
            cost = j * C1 + t2 * C2
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
