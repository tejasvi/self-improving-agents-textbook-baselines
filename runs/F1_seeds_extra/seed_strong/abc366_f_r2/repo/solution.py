import sys
from fractions import Fraction


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    cnt = {}
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        key = (a, b)
        c = cnt.get(key, 0)
        if c < k:
            cnt[key] = c + 1
    items = []
    for (a, b), c in cnt.items():
        kf = Fraction(a - 1, b)
        for _ in range(c):
            items.append((kf, a, b))
    # Innermost function is applied first: process in ascending order of (A-1)/B.
    items.sort(key=lambda t: t[0])
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
