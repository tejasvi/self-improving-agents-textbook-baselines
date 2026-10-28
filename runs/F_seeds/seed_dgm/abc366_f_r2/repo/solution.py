import sys
from fractions import Fraction


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    # Keep at most k copies of each (A, B) pair; more copies are never useful.
    cnt = {}
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        c = cnt.get((a, b), 0)
        if c < k:
            cnt[(a, b)] = c + 1

    items = []
    for (a, b), c in cnt.items():
        for _ in range(c):
            items.append((a, b))

    # Exchange argument: applying i inner and j outer is better than the reverse
    # iff B_i/(A_i-1) >= B_j/(A_j-1) (A=1 treated as +infinity).

    def key(item):
        a, b = item
        if a == 1:
            return (1, Fraction(0))
        return (0, Fraction(b, a - 1))

    # Sort so that items with larger key are applied first (innermost).
    items.sort(key=key, reverse=True)

    dp = [None] * (k + 1)
    dp[0] = 1  # x = 1 initially
    for a, b in items:
        for j in range(k - 1, -1, -1):
            if dp[j] is not None:
                v = a * dp[j] + b
                if dp[j + 1] is None or v > dp[j + 1]:
                    dp[j + 1] = v
    print(dp[k])


main()
