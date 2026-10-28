import sys
from fractions import Fraction


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    funcs = []
    INF = Fraction(10 ** 9)
    idx = 2
    for _ in range(n):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        key = INF if a == 1 else Fraction(b, a - 1)
        funcs.append((key, a, b))
    # Apply functions with larger b/(a-1) first (applied earlier in time).
    funcs.sort(key=lambda t: t[0], reverse=True)

    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for _, a, b in funcs:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev is not NEG:
                v = a * prev + b
                if dp[j] is NEG or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
