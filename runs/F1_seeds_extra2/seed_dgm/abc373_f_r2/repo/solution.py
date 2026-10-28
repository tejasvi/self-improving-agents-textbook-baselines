import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    by_weight = defaultdict(list)
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        if w <= W:
            by_weight[w].append(v)

    items = []  # (weight, gain)
    for w, vs in by_weight.items():
        K = W // w
        gains = []
        for v in vs:
            # k-th copy gain: v - 2k + 1, positive only; at most K copies
            cnt = min(K, (v + 1) // 2)  # number of k>=1 with v-2k+1>0
            gains.extend(v - 2 * k + 1 for k in range(1, cnt + 1))
        if not gains:
            continue
        gains.sort(reverse=True)
        for g in gains[:K]:
            if g <= 0:
                break
            items.append((w, g))

    dp = [0] * (W + 1)  # dp[c] = best value with total weight <= c
    for w, g in items:
        # 0/1 knapsack step, using the old dp for all reads
        dp[w:] = [a if a >= b + g else b + g
                  for a, b in zip(dp[w:], dp[:W + 1 - w])]
    print(dp[W])


main()
