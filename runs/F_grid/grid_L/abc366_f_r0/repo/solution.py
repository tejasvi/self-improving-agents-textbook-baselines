import sys
from fractions import Fraction
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    cnt = Counter()
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        cnt[(a, b)] += 1

    # Only up to K copies of each (A, B) pair can ever be useful.
    items = []
    for (a, b), c in cnt.items():
        for _ in range(min(c, k)):
            items.append((a, b))

    # Application order: g applied before f iff B_g*(A_f-1) >= B_f*(A_g-1).
    # Sort by key B/(A-1) descending; A=1 functions (infinite key) come first.
    def key(item):
        a, b = item
        if a == 1:
            return (0, Fraction(0))
        return (1, Fraction(-b, a - 1))

    items.sort(key=key)

    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in items:
        for j in range(k, 0, -1):
            if dp[j - 1] is not None:
                v = a * dp[j - 1] + b
                if dp[j] is None or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
