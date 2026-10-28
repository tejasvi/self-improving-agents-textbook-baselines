import sys
import heapq
from itertools import repeat
from operator import add


def main():
    data = sys.stdin.buffer.read().split()
    n, W = int(data[0]), int(data[1])
    groups = {}
    idx = 2
    for _ in range(n):
        w = int(data[idx]); v = int(data[idx + 1]); idx += 2
        groups.setdefault(w, []).append(v)

    # Marginal gain of the k-th copy of an item with value v is v + 1 - 2k,
    # strictly decreasing in k, so for a fixed weight we only need the top
    # K = W // w marginals across all types with that weight (concave gains).
    dp = [0] * (W + 1)
    for w, vs in groups.items():
        K = W // w
        cand = []
        for v in vs:
            kmax = min(K, v // 2)  # v + 1 - 2k > 0  <=>  k <= v // 2
            cand.extend(range(v + 1 - 2, v - 2 * kmax, -2))
        if not cand:
            continue
        if len(cand) > K:
            cand = heapq.nlargest(K, cand)
        else:
            cand.sort(reverse=True)
        pref = [0]
        s = 0
        for m in cand:
            s += m
            pref.append(s)
        new = dp[:]
        for m in range(1, len(pref)):
            sh = m * w
            if sh > W:
                break
            new[sh:] = list(map(max, new[sh:], map(add, dp, repeat(pref[m]))))[:W + 1 - sh]
        dp = new
    print(dp[W])


main()
