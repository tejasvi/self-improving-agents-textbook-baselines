import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    items = []
    for i in range(n):
        a = int(data[2 + 2 * i]); b = int(data[3 + 2 * i])
        key = b / (a - 1) if a > 1 else 1e9
        items.append((key, a, b))
    # Inner functions are processed first: larger key = more inner.
    items.sort(key=lambda t: t[0], reverse=True)
    NEG = -1
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for _, a, b in items:
        for j in range(k - 1, -1, -1):
            v = dp[j]
            if v >= 0:
                nv = a * v + b
                if nv > dp[j + 1]:
                    dp[j + 1] = nv
    print(dp[k])

main()
