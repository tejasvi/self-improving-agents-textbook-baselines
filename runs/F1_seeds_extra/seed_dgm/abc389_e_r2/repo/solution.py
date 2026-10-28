import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    # Buying the k-th unit of product i costs (2k-1)*P_i; buying c units costs
    # P_i*c^2 in total. Greedily take the cheapest marginal costs overall.
    # For threshold T, product i contributes c_i(T) = number of odd j with
    # j*P_i <= T, i.e. c_i = (T // P_i + 1) // 2.

    def count(T):
        return sum(((T // p) + 1) >> 1 for p in P)

    def cost(T, limit):
        """Total cost of marginal units <= T; returns None once it exceeds limit."""
        s = 0
        for p in P:
            c = ((T // p) + 1) >> 1
            if c:
                s += p * c * c
                if s > limit:
                    return None
        return s

    # Largest T with S(T) <= m (S is nondecreasing). S(0)=0.
    # S(2*10^14) > 10^18 >= m since S(T) >= T^2 / (8*10^9) roughly.
    lo, hi = 0, 2 * 10**14
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost(mid, m) is not None:
            lo = mid
        else:
            hi = mid
    T = lo
    S_T = cost(T, m) if T > 0 else 0
    cnt_T = count(T)
    add_count = count(T + 1) - cnt_T
    budget = m - S_T
    extra = min(add_count, budget // (T + 1))
    print(cnt_T + extra)


main()
