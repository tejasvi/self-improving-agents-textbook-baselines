import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    items = []
    inf = float("inf")
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        # Applied-first (inner) functions have larger key.
        key = inf if a == 1 else b / (a - 1)
        items.append((key, a, b))
    # Sort so that the inner-most function (applied first) comes first.
    items.sort(key=lambda t: -t[0])

    NEG = -1
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for _, a, b in items:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev >= 0:
                v = a * prev + b
                if v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
