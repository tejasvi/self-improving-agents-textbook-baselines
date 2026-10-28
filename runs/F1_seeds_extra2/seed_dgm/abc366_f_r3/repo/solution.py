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

    # f applied before g (f inner) iff B_f*(A_g-1) > B_g*(A_f-1)
    def cmp(f, g):
        lhs = f[1] * (g[0] - 1)
        rhs = g[1] * (f[0] - 1)
        if lhs > rhs:
            return -1
        if lhs < rhs:
            return 1
        return 0

    funcs.sort(key=cmp_to_key(cmp))

    NEG = None
    dp = [NEG] * (k + 1)  # dp[j]: best value using j chosen functions
    dp[0] = 1
    for a, b in funcs:
        for j in range(k, 0, -1):
            if dp[j - 1] is not None:
                v = a * dp[j - 1] + b
                if dp[j] is None or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
