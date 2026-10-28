import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def evaluate(T):
        # cost of taking all marginal units with price <= T; None if over budget
        cost = 0
        cnt = 0
        for p in P:
            c = ((T // p) + 1) >> 1
            if c:
                cnt += c
                cost += c * c * p
                if cost > m:
                    return None
        return cnt, cost

    lo, hi = 0, 2 * 10**14 + 10
    while lo < hi:
        mid = (lo + hi + 1) >> 1
        if evaluate(mid) is not None:
            lo = mid
        else:
            hi = mid - 1
    cnt, cost = evaluate(lo)
    print(cnt + (m - cost) // (lo + 1))

main()
