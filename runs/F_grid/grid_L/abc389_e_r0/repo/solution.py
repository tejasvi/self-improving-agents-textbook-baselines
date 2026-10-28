import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    ps = [int(x) for x in data[2:2 + n]]

    # Buying the k-th unit of product i costs (2k-1)*P_i (marginal cost),
    # which is increasing in k. So the optimal purchase is the cheapest
    # prefix of all marginal costs. Let S(X) = total cost of all marginal
    # costs <= X, and c(X) = their count. S(X) = sum P_i * c_i^2 where
    # c_i = number of odd multiples of P_i that are <= X.

    def count_and_sum(x):
        cnt = 0
        total = 0
        for p in ps:
            c = ((x // p) + 1) >> 1
            if c:
                cnt += c
                total += p * c * c
        return cnt, total

    lo, hi = 0, 4 * 10 ** 18  # S(lo) <= M, S(hi) > M
    while hi - lo > 1:
        mid = (lo + hi) // 2
        s = 0
        ok = True
        for p in ps:
            c = ((mid // p) + 1) >> 1
            if c:
                s += p * c * c
                if s > m:
                    ok = False
                    break
        if ok:
            lo = mid
        else:
            hi = mid

    cnt, total = count_and_sum(lo)
    rem = m - total
    # Items with marginal cost exactly lo+1 are the next ones; fewer than
    # all of them fit in the remaining budget, so floor division is valid.
    cnt += rem // (lo + 1)
    print(cnt)


main()
