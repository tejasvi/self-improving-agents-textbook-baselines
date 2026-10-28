import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    ps = [int(x) for x in data[2:2 + n]]

    # Marginal cost of the k-th unit of product i is (2k-1)*P_i.
    # Items with cost <= T for product i: k with (2k-1)*P_i <= T,
    # i.e. c_i = floor((floor(T/P_i)+1)/2) units, total cost c_i^2 * P_i.
    def stats(t):
        cnt = 0
        total = 0
        for p in ps:
            q = t // p
            if q == 0:
                continue
            c = (q + 1) >> 1
            cnt += c
            total += c * c * p
        return cnt, total

    # Largest T with A(T) <= M (A(T) = total cost of items with cost <= T).
    lo, hi = 0, 4 * 10**18  # A(0)=0 <= M; A(hi) > M
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if stats(mid)[1] <= m:
            lo = mid
        else:
            hi = mid
    t = lo
    cnt, total = stats(t)
    remaining = m - total
    # Items with cost exactly t+1 cost t+1 each; fewer than all of them fit.
    answer = cnt + remaining // (t + 1)
    print(answer)


if __name__ == "__main__":
    main()
