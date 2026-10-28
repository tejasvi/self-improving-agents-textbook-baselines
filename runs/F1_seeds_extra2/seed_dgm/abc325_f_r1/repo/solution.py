import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3

    INF = 10 ** 18
    # dp[j] = min number of type-2 sensors to cover processed sections using exactly j type-1 sensors
    dp = [INF] * (K1 + 1)
    dp[0] = 0
    for d in D:
        # maximum useful type-1 sensors for this section
        A = min(K1, (d + L1 - 1) // L1)
        new = [INF] * (K1 + 1)
        for a in range(A + 1):
            rem = d - a * L1
            ga = (rem + L2 - 1) // L2 if rem > 0 else 0
            seg = [x + ga for x in dp[:K1 + 1 - a]]
            new[a:] = map(min, new[a:], seg)
        # prune states that already exceed the type-2 budget
        dp = [v if v <= K2 else INF for v in new]

    best = -1
    for j in range(K1 + 1):
        if dp[j] <= K2:
            cost = C1 * j + C2 * dp[j]
            if best < 0 or cost < best:
                best = cost
    print(best)


main()
