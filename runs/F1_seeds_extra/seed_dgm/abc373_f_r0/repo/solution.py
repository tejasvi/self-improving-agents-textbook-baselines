import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    groups = {}
    for i in range(n):
        w = int(data[2 + 2 * i])
        v = int(data[3 + 2 * i])
        groups.setdefault(w, []).append(v)

    NEG = None
    dp = [0] * (W + 1)  # dp[c] = best happiness with weight at most c
    for w, vs in groups.items():
        K = W // w
        if K <= 0:
            continue
        # The j-th copy (j>=1) of a type with value v has marginal gain v - 2j + 1,
        # strictly decreasing in j, so taking copies greedily by gain is optimal.
        # Within one weight class only the top K positive gains can ever be used.
        cand = []
        for v in vs:
            j = 1
            while j <= K:
                g = v - 2 * j + 1
                if g <= 0:
                    break
                cand.append(g)
                j += 1
        if len(cand) > K:
            cand = heapq.nlargest(K, cand)
        for g in cand:
            # 0/1 knapsack step (descending order handled by building a new list)
            shifted = [x + g for x in dp[:W + 1 - w]]
            dp[w:] = list(map(max, dp[w:], shifted))
    print(dp[W])


main()
