import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    ds = [int(data[idx + i]) for i in range(n)]
    idx += n
    l1, c1, k1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    l2, c2, k2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])

    INF = 10 ** 18
    # dp[A] = minimum number of type-2 sensors when exactly A type-1 sensors used
    dp = [INF] * (k1 + 1)
    dp[0] = 0
    for d in ds:
        cmax = min((d + l1 - 1) // l1, k1)
        new = [INF] * (k1 + 1)
        for a in range(cmax + 1):
            rem = d - a * l1
            b = (rem + l2 - 1) // l2 if rem > 0 else 0
            seg = [x + b for x in dp[:k1 + 1 - a]]
            new[a:] = map(min, new[a:], seg)
        dp = new

    best = -1
    for A in range(k1 + 1):
        if dp[A] <= k2:
            cost = c1 * A + c2 * dp[A]
            if best < 0 or cost < best:
                best = cost
    print(best)


main()
