import sys
from functools import lru_cache


def main():
    N, A, X, Y = map(int, sys.stdin.read().split())
    sys.setrecursionlimit(10000)

    # f(n) = min(X + f(n//A), (6Y + sum_{b=2..6} f(n//b)) / 5)
    # (die option solved from the self-loop when b = 1)
    @lru_cache(maxsize=None)
    def f(n):
        if n == 0:
            return 0.0
        a = X + f(n // A)
        c = sum(f(n // b) for b in range(2, 7))
        d = (6 * Y + c) / 5.0
        return min(a, d)

    print("%.15f" % f(N))


main()
