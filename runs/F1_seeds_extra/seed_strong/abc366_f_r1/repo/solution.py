import sys
from functools import cmp_to_key
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    cnt = Counter()
    idx = 2
    for _ in range(n):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        cnt[(a, b)] += 1
    items = []
    for (a, b), c in cnt.items():
        for _ in range(min(c, k)):
            items.append((a, b))

    # a is applied before (inner to) b iff B_a*(A_b-1) >= B_b*(A_a-1)
    def cmp(x, y):
        lhs = x[1] * (y[0] - 1)
        rhs = y[1] * (x[0] - 1)
        if lhs > rhs:
            return -1
        if lhs < rhs:
            return 1
        return 0

    items.sort(key=cmp_to_key(cmp))
    NEG = -1
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in items:
        for j in range(k, 0, -1):
            if dp[j - 1] >= 0:
                v = a * dp[j - 1] + b
                if v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
