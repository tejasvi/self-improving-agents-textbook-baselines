import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    items = []
    inf = float('inf')
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        key = inf if a == 1 else b / (a - 1)
        items.append((key, a, b))
    # inner-applied-first order: descending key
    items.sort(key=lambda t: -t[0])
    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for _, a, b in items:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev is not None:
                v = a * prev + b
                if dp[j] is None or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
