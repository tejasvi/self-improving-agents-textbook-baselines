import sys
from math import isqrt

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]
    Pmin = min(P)

    def counts(X):
        return [((X // p) + 1) >> 1 for p in P]

    def cost_ok(X):
        s = 0
        for p in P:
            c = ((X // p) + 1) >> 1
            s += p * c * c
            if s > M:
                return False
        return True

    # Upper bound: with X = 2*isqrt(M*Pmin)+2... use a safe bound where cost exceeds M
    lo, hi = 0, 4 * isqrt(M * Pmin) + 10
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost_ok(mid):
            lo = mid
        else:
            hi = mid
    X = lo
    total_cnt = 0
    cost = 0
    for p in P:
        c = ((X // p) + 1) >> 1
        total_cnt += c
        cost += p * c * c
    R = M - cost
    print(total_cnt + R // (X + 1))

main()
