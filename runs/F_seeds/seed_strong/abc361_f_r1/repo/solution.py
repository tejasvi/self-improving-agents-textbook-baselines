import sys


def iroot(n, k):
    # floor of n^(1/k), exact
    if k == 1:
        return n
    r = int(round(n ** (1.0 / k)))
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
        mu = mobius(k)
        if mu == 0:
            continue
        r = iroot(n, k)
        if r < 2:
            break
        total += -mu * (r - 1)
    print(total + 1)


main()
