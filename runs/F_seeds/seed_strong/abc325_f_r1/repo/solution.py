import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    D = [int(data[idx + i]) for i in range(n)]
    idx += n
    L1, C1, K1 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2]); idx += 3
    L2, C2, K2 = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
    BIG = 10 ** 9
    # dp[t] = min number of type-2 sensors using exactly/at most t type-1 sensors so far
    dp = [BIG] * (K1 + 1)
    dp[0] = 0
    for d in D:
        # maximum useful type-1 count for this section
        amax = min(K1, -(-d // L1))
        # options: (a, b) with b minimal for that a; keep only where b strictly decreases
        opts = []
        prev_b = None
        for a in range(amax + 1):
            rem = d - a * L1
            b = -(-rem // L2) if rem > 0 else 0
            if prev_b is None or b < prev_b:
                opts.append((a, b))
                prev_b = b
            if b == 0:
                break
        new = [BIG] * (K1 + 1)
        for a, b in opts:
            # new[t] = min(new[t], dp[t-a] + b) for t >= a
            new[a:] = map(min, new[a:], map(b.__add__, dp))
        # cap at BIG (values above K2 are infeasible anyway)
        dp = [v if v <= K2 else BIG for v in new]
    best = None
    for t in range(K1 + 1):
        if dp[t] <= K2:
            cost = t * C1 + dp[t] * C2
            if best is None or cost < best:
                best = cost
    print(-1 if best is None else best)


main()
