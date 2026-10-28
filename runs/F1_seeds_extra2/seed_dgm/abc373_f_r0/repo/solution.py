import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    groups = {}  # weight -> list of marginal values
    idx = 2
    for _ in range(n):
        w = int(data[idx]); v = int(data[idx + 1]); idx += 2
        K = W // w
        if K == 0:
            continue
        # k-th copy (0-based) has marginal gain v - 1 - 2k; keep only positive ones
        lst = groups.setdefault(w, [])
        for k in range(K):
            c = v - 1 - 2 * k
            if c <= 0:
                break
            lst.append(c)

    # Items of the same weight: at most W//w of them can ever be used.
    items = []
    for w, lst in groups.items():
        M = W // w
        if len(lst) > M:
            lst.sort(reverse=True)
            del lst[M:]
        for c in lst:
            items.append((w, c))

    # 0/1 knapsack over unit items with weights w and values c.
    dp = [0] * (W + 1)
    for w, c in items:
        # new dp[j] = max(dp[j], dp[j-w] + c) for j >= w
        shifted = [x + c for x in dp[:W + 1 - w]]
        dp[w:] = [a if a >= b else b for a, b in zip(dp[w:], shifted)]
    print(max(dp))


main()
