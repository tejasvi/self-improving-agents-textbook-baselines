import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    items = []
    inf = float("inf")
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        # Inner (earlier-applied) functions come first: sort by B/(A-1) descending.
        key = inf if a == 1 else b / (a - 1)
        items.append((-key, a, b))
    items.sort()
    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for _, a, b in items:
        for t in range(k - 1, -1, -1):
            v = dp[t]
            if v is not None:
                nv = a * v + b
                cur = dp[t + 1]
                if cur is None or nv > cur:
                    dp[t + 1] = nv
    print(dp[k])


main()
