import sys
from functools import cmp_to_key


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    items = []
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        items.append((a, b))

    # Inner function i should come before outer j iff B_i*(A_j-1) > B_j*(A_i-1)
    def cmp(p, q):
        a1, b1 = p
        a2, b2 = q
        l = b1 * (a2 - 1)
        r = b2 * (a1 - 1)
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
