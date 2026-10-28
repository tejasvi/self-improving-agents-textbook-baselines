import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    items = []
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        # Sort so the function applied first (innermost) comes first, by key -b/(a-1).
        # a == 1 functions use -inf so they come first.
        key = float('-inf') if a == 1 else -b / (a - 1)
        items.append((key, a, b))
    items.sort()

    # dp[j] = max value obtainable applying j chosen functions (in sorted order) to 1.
    dp = [None] * (k + 1)
    dp[0] = 1
    for _, a, b in items:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev is not None:
                cand = a * prev + b
                if dp[j] is None or cand > dp[j]:
                    dp[j] = cand
    print(dp[k])


main()
