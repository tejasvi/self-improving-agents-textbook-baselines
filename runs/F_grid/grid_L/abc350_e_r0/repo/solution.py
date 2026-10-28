import sys
from functools import lru_cache


def main():
    N, A, X, Y = map(int, sys.stdin.read().split())
    sys.setrecursionlimit(10000)

    # E(n) = min(X + E(n//A), (6Y + sum_{b=2..6} E(n//b)) / 5)
    # The die option is self-looping on outcome 1, which gives the 6/5 factor.
    @lru_cache(maxsize=None)
    def E(n):
        if n == 0:
            return 0.0
        via_op = X + E(n // A)
        s = 0.0
        for b in range(2, 7):
            s += E(n // b)
        via_die = (6.0 * Y + s) / 5.0
        return min(via_op, via_die)

    print("%.15f" % E(N))


main()
