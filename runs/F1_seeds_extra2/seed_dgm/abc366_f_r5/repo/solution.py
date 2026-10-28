import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    funcs = []
    idx = 2
    for _ in range(n):
        funcs.append((int(data[idx]), int(data[idx + 1])))
        idx += 2

    # Exchange argument: g applied before h is better iff
    # B_g*(A_h-1) > B_h*(A_g-1). This is ordering by B/(A-1) descending,
    # with A=1 functions first (they are "infinitely" good to apply first).
    def key(f):
        a, b = f
        if a == 1:
            return (0, 0.0)
        return (1, -b / (a - 1))

    funcs.sort(key=key)

    # dp[j] = max value after applying j chosen functions (in sorted order)
    dp = [None] * (k + 1)
    dp[0] = 1
    for a, b in funcs:
        for j in range(k - 1, -1, -1):
            v = dp[j]
            if v is not None:
                nv = a * v + b
                cur = dp[j + 1]
                if cur is None or nv > cur:
                    dp[j + 1] = nv
    print(dp[k])


main()
