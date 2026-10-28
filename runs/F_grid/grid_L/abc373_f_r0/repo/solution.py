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

    NEG = -(1 << 62)
    dp = [0] * (W + 1)  # dp[c]: max happiness with total weight <= c

    for w, vals in groups.items():
        M = W // w
        if M == 0:
            continue
        # Top M positive marginal values among all copies of items with weight w.
        # Copy k (1-based) of a type with value v has marginal v - 2k + 1.
        vals.sort(reverse=True)
        heap = []
        for idx, v in enumerate(vals):
            if v - 1 > 0:
                heap.append((-(v - 1), idx, 1))
        heapq.heapify(heap)
        marg = []
        while heap and len(marg) < M:
            negm, idx, k = heapq.heappop(heap)
            marg.append(-negm)
            nv = vals[idx] - 2 * (k + 1) + 1
            if nv > 0:
                heapq.heappush(heap, (-nv, idx, k + 1))
        if not marg:
            continue
        T = len(marg)
        # G[t] = best profit using t items of weight w (capped at T; concave).
        G = [0] * (M + 1)
        acc = 0
        for t in range(1, M + 1):
            if t <= T:
                acc += marg[t - 1]
            G[t] = acc

        for r in range(min(w, W + 1)):
            a = dp[r::w]
            L = len(a)
            b = [0] * L
            # Divide and conquer over j with monotone optimal s.
            stack = [(0, L - 1, 0, L - 1)]
            while stack:
                lo, hi, olo, ohi = stack.pop()
                if lo > hi:
                    continue
                mid = (lo + hi) >> 1
                best = NEG
                bs = olo
                upper = mid if mid < ohi else ohi
                for s in range(olo, upper + 1):
                    val = a[s] + G[mid - s if mid - s <= M else M]
                    if val > best:
                        best = val
                        bs = s
                b[mid] = best
                stack.append((lo, mid - 1, olo, bs))
                stack.append((mid + 1, hi, bs, ohi))
            dp[r::w] = b

    print(dp[W])


main()
