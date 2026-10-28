import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    funcs = []
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        funcs.append((a, b))

    # Exchange argument: applying i (inner) before j (outer) is at least as good
    # as the reverse iff B_i*(A_j-1) >= B_j*(A_i-1).
    def cmp(x, y):
        ax, bx = x
        ay, by = y
        l = bx * (ay - 1)
        r = by * (ax - 1)
        if l > r:
            return -1
        if l < r:
            return 1
        return 0

    funcs.sort(key=cmp_to_key(cmp))

    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in funcs:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev is not None:
                v = a * prev + b
                if dp[j] is None or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
