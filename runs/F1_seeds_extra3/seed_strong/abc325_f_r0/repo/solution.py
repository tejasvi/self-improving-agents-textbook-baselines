import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = float('inf')
    if sum(D) > K1 * L1 + K2 * L2:
        print(-1)
        return
    # dp[x] = min number of type-2 sensors, using at most x type-1 sensors
    dp = [0] * (K1 + 1)
    for d in D:
        amax = min(K1, (d + L1 - 1) // L1)
        # candidate (a, b): keep only the smallest a for each distinct b
        cands = []
        last_b = None
        for a in range(amax + 1):
            rem = d - a * L1
            b = (rem + L2 - 1) // L2 if rem > 0 else 0
            if b > K2:
                continue
            if b != last_b:
                cands.append((a, b))
                last_b = b
        new = [INF] * (K1 + 1)
        for a, b in cands:
            for x in range(a, K1 + 1):
                v = dp[x - a] + b
                if v < new[x]:
                    new[x] = v
        dp = new
        if all(v == INF for v in dp):
            print(-1)
            return

    best = None
    for x in range(K1 + 1):
        if dp[x] <= K2:
            cost = C1 * x + C2 * dp[x]
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
