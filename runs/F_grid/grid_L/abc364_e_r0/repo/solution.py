import sys


def main():
    data = sys.stdin.read().split()
    n, X, Y = int(data[0]), int(data[1]), int(data[2])
    items = []
    for i in range(n):
        a = int(data[3 + 2 * i])
        b = int(data[4 + 2 * i])
        items.append((a, b))

    # Snuke always eats the dishes of a prefix of the arrangement. If a set S of
    # dishes has total sweetness <= X and total saltiness <= Y, Snuke eats all of
    # S and then at least one more dish (the next one, if it exists).
    # Conversely, the eaten prefix minus its last dish is such a feasible set.
    # Hence answer = min(N, m + 1), where m is the largest feasible subset size.
    #
    # dp[c][s] = minimum total saltiness over subsets of size c with sweetness
    # exactly s (0 <= s <= X). INF marks unreachable states.
    INF = 1 << 30
    dp = [[INF] * (X + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    cnt = 0
    for a, b in items:
        if a > X:
            continue
        cnt += 1
        for c in range(cnt - 1, -1, -1):
            src = dp[c]
            dst = dp[c + 1]
            # dst[s + a] = min(dst[s + a], src[s] + b) for s in [0, X - a]
            shifted = [v + b if v < INF else INF for v in src[:X + 1 - a]]
            dst[a:] = map(min, dst[a:], shifted)

    m = 0
    for c in range(n + 1):
        if min(dp[c]) <= Y:
            m = c
    print(min(n, m + 1))


main()
