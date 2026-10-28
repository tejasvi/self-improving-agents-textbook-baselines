import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    W = int(data[1])
    groups = {}
    idx = 2
    for _ in range(n):
        w = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        if w <= W:
            groups.setdefault(w, []).append(v)

    dp = [0] * (W + 1)
    for w, vs in groups.items():
        K = W // w
        # Marginal gain of the k-th item of a type with value v: g_k = v - 2k + 1 (k = 1..K),
        # strictly decreasing in k, so the chosen candidates are the top-K positive gains
        # over all types with weight w.

        def count_ge(T):
            # number of marginals >= T (T >= 1), capped per type at K
            total = 0
            for v in vs:
                c = (v - T + 1) // 2
                if c > 0:
                    total += c if c < K else K
            return total

        # Largest T >= 1 with count_ge(T) >= K; if none, take all positive marginals.
        if count_ge(1) <= K:
            T = 1
        else:
            lo, hi = 1, max(vs)  # count_ge(lo) > K, find max T with count_ge(T) >= K
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if count_ge(mid) >= K:
                    lo = mid
                else:
                    hi = mid - 1
            T = lo
        # Gather marginals strictly greater than T (fewer than K), then fill with T.
        marg = []
        for v in vs:
            c = (v - T) // 2  # marginals >= T+1
            if c > 0:
                marg.extend(v - 2 * k + 1 for k in range(1, min(c, K) + 1))
        need = K - len(marg)
        if need > 0 and count_ge(T) > 0:
            # Fill with copies of T (only those counted by count_ge(T)).
            marg.extend([T] * min(need, count_ge(T) - len(marg)))
        # 0/1 knapsack over each candidate item of weight w
        for val in marg:
            shifted = [x + val for x in dp[:W + 1 - w]]
            dp[w:] = [a if a >= b else b for a, b in zip(dp[w:], shifted)]
    print(dp[W])


main()
