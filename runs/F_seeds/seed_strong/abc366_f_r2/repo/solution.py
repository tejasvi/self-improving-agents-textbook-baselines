import sys
from collections import Counter
from functools import cmp_to_key


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    cnt = Counter()
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        cnt[(a, b)] += 1
    items = []
    for (a, b), c in cnt.items():
        for _ in range(min(c, k)):
            items.append((a, b))

    # Inner-first order: x before y iff B_x*(A_y-1) >= B_y*(A_x-1)
    def cmp(x, y):
        l = x[1] * (y[0] - 1)
        r = y[1] * (x[0] - 1)
        if l > r:
            return -1
        if l < r:
            return 1
        return 0

    items.sort(key=cmp_to_key(cmp))

    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in items:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev is not None:
                v = a * prev + b
                if dp[j] is None or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
