import sys


def main():
    data = sys.stdin.read().split()
    n, X, Y = int(data[0]), int(data[1]), int(data[2])
    items = []
    for i in range(n):
        items.append((int(data[3 + 2 * i]), int(data[4 + 2 * i])))

    INF = float("inf")
    # dp[k][s] = minimum total saltiness over subsets of size k
    # with total sweetness exactly s (0 <= s <= X).
    dp = [[INF] * (X + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    cnt = 0
    for a, b in items:
        cnt += 1
        if a > X:
            continue  # such a dish can never be among the first k-1 eaten
        for k in range(cnt - 1, -1, -1):
            src = dp[k]
            tgt = dp[k + 1]
            # tgt[s + a] = min(tgt[s + a], src[s] + b)
            shifted = [INF] * a + [v + b for v in src[: X + 1 - a]]
            dp[k + 1] = list(map(min, tgt, shifted))
    best = 0
    for k in range(n + 1):
        if min(dp[k]) <= Y:
            best = k
    # Snuke eats best dishes that fit, plus one more (the overflowing dish), if any remain.
    print(min(n, best + 1))


main()
