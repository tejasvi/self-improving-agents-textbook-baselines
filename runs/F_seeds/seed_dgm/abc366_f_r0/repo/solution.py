import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    funcs = []
    idx = 2
    for _ in range(n):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        funcs.append((a, b))

    # f applied before g (f innermost) is better iff
    # B_f*(A_g-1) > B_g*(A_f-1); sort so that such pairs come first.
    def cmp(f, g):
        lhs = f[1] * (g[0] - 1)
        rhs = g[1] * (f[0] - 1)
        if lhs > rhs:
            return -1
        if lhs < rhs:
            return 1
        return 0

    funcs.sort(key=cmp_to_key(cmp))

    NEG = -1
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in funcs:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev >= 0:
                cand = a * prev + b
                if cand > dp[j]:
                    dp[j] = cand
    print(dp[k])


main()
