import sys


def mobius(k):
    res = 1
    d = 2
    while d * d <= k:
        if k % d == 0:
            k //= d
            if k % d == 0:
                return 0
            res = -res
        d += 1
    if k > 1:
        res = -res
    return res


def iroot(n, k):
    """Largest r with r**k <= n."""
    r = int(round(n ** (1.0 / k)))
    while r > 0 and r ** k > n:
        r -= 1
    while (r + 1) ** k <= n:
        r += 1
    return r


def main():
    N = int(sys.stdin.readline())
    # count of perfect powers >1 in [2, N] via Mobius inversion, plus 1 for the number 1
    total = 0
    for k in range(2, 64):
        m = mobius(k)
        if m == 0:
            continue
        r = iroot(N, k)
        if r < 2:
            continue
        total += -m * (r - 1)
    print(total + 1)


main()
