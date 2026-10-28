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
        if w > W:
            continue
        groups.setdefault(w, []).append(v)

    # The k-th copy of a type with value v has marginal gain v - (2k - 1),
    # strictly decreasing in k. Copies of all types with weight w have the
    # same weight, so for each weight class we only need the top W // w
    # marginal gains (taken greedily, which keeps each type's picks a prefix).
    dp = [0] * (W + 1)  # dp[j] = best total happiness with weight <= j
    for w, vs in groups.items():
        cap = W // w
        # Greedy merge: heap of (-next_gain, type_index, k_next)
        heap = [(-(v - 1), i, 1) for i, v in enumerate(vs) if v - 1 > 0]
        heapq.heapify(heap)
        top = []
        while heap and len(top) < cap:
            negg, i, k = heapq.heappop(heap)
            g = -negg
            top.append(g)
            nk = k + 1
            ng = vs[i] - 2 * nk + 1
            if ng > 0:
                heapq.heappush(heap, (-ng, i, nk))
        if not top:
            continue
        P = [0]
        for g in top:
            P.append(P[-1] + g)
        new = dp[:]
        for c in range(1, len(top) + 1):
            s = c * w
            if s > W:
                break
            cand = map(add, dp[:W + 1 - s], repeat(P[c]))
            new[s:] = list(map(max, new[s:], cand))
        dp = new

    print(dp[W])


main()
