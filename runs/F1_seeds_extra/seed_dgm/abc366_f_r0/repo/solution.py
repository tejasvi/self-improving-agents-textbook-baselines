import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    funcs = []
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        funcs.append((a, b))

    # i should be applied before j iff B_i*(A_j-1) >= B_j*(A_i-1)
    def cmp(x, y):
        lhs = x[1] * (y[0] - 1)
        rhs = y[1] * (x[0] - 1)
        if lhs > rhs:
            return -1
        if lhs < rhs:
            return 1
        return 0

    funcs.sort(key=cmp_to_key(cmp))

    NEG = -1
    dp = [NEG] * (k + 1)  # dp[j]: best value using j functions from prefix
    dp[0] = 1
    for a, b in funcs:
        for j in range(k, 0, -1):
            if dp[j - 1] >= 0:
                v = a * dp[j - 1] + b
                if v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
