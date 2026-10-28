import sys
from fractions import Fraction


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    items = []
    idx = 2
    for _ in range(n):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        items.append((a, b))
    # Innermost function is applied first; it should have the smallest (A-1)/B.
    items.sort(key=lambda t: Fraction(t[0] - 1, t[1]))
    NEG = -1
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in items:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev >= 0:
                cand = a * prev + b
                if cand > dp[j]:
                    dp[j] = cand
    print(dp[k])


if __name__ == "__main__":
    main()
