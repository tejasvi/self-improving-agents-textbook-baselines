import sys


def iroot(n, k):
    """Largest integer r with r**k <= n."""
    if k == 1:
        return n
    r = int(round(n ** (1.0 / k)))
    # adjust using exact integer arithmetic
    while r > 0 and r ** k > n:
        r -= 1
    while (r + 1) ** k <= n:
        r += 1
    return r


def mobius(k):
    res = 1
    d = 2
    m = k
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            res = -res
        d += 1
    if m > 1:
        res = -res
    return res


def main():
    n = int(sys.stdin.read().split()[0])
    total = 0
    for k in range(2, 64):
        if (1 << k) > n and k > 2:
            break
        mu = mobius(k)
        if mu == 0:
            continue
        total += -mu * (iroot(n, k) - 1)
    # total counts perfect powers in [2, n]; add 1 for x = 1
    print(total + 1 if n >= 1 else 0)


main()
