import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    by_weight = {}
    idx = 2
    for _ in range(n):
        w = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        by_weight.setdefault(w, []).append(v)

    # Every item of weight w is interchangeable; the k-th item taken from
    # type i has marginal v_i - (2k-1), decreasing in k. So a 0/1 knapsack
    # over all positive marginals (capped at W // w per weight class) is exact.
    dp = [0] * (W + 1)  # dp[c] = best value with total weight <= c
    for w, vs in by_weight.items():
        K = W // w
        if K == 0:
            continue
        marg = []
        for v in vs:
            # k = 1..K ; marginal = v - (2k-1) > 0
            k = 1
            while k <= K:
                m = v - (2 * k - 1)
                if m <= 0:
                    break
                marg.append(m)
                k += 1
        if not marg:
            continue
        marg.sort(reverse=True)
        del marg[K:]
        for m in marg:
            # 0/1 knapsack step for one item of weight w and value m
            dp[w:] = [a if a >= b + m else b + m
                      for a, b in zip(dp[w:], dp)]
    print(dp[W])


main()
