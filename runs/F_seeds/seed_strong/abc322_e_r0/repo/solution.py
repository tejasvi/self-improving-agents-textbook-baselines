import sys
from itertools import product


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    pos = 3
    base = p + 1
    S = base ** k
    # Weights for mixed-radix encoding: state index = sum d_j * base^j
    weights = [base ** j for j in range(k)]
    # digit tuples for every state index
    digit_lists = [[] for _ in range(k)]
    # build digits per state: state s -> (d_0..d_{k-1})
    states = []
    for tup in product(range(base), repeat=k):
        # product iterates last coordinate fastest; convert to index
        idx = 0
        for j in range(k):
            idx += tup[j] * weights[j]
        states.append((idx, tup))
    # ordering array: column j of states by index
    digits_by_idx = [None] * S
    for idx, tup in states:
        digits_by_idx[idx] = tup
    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for _ in range(n):
        c = int(data[pos])
        a = [int(x) for x in data[pos + 1:pos + 1 + k]]
        pos += 1 + k
        # per-parameter lookup: T[j][d] = min(d+a_j, p) * w_j
        T = [[min(d + a[j], p) * weights[j] for d in range(base)] for j in range(k)]
        new = dp[:]
        for s in range(S):
            v = dp[s]
            if v == INF:
                continue
            d = digits_by_idx[s]
            t = 0
            for j in range(k):
                t += T[j][d[j]]
            nv = v + c
            if nv < new[t]:
                new[t] = nv
        dp = new
    ans = dp[S - 1]  # all parameters equal to p
    print(ans if ans != INF else -1)


main()
