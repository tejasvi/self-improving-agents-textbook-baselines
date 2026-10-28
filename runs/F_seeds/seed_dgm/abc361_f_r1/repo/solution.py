import sys


def iroot(n, k):
    """Largest integer r with r**k <= n (exact)."""
    if n < 2:
        return n
    r = int(round(n ** (1.0 / k)))
    # correct floating-point error
    while r > 0 and r ** k > n:
        r -= 1
    while (r + 1) ** k <= n:
        r += 1
    return r


def mobius(n):
    res = 1
    d = 2
    m = n
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
    N = int(sys.stdin.read().split()[0])
    # count perfect powers in [2, N]
    total = 0
    for b in range(2, N.bit_length() + 2):
        mu = mobius(b)
        if mu == 0:
            continue
        r = iroot(N, b)
        if r < 2:
            break
        total += -mu * (r - 1)
    # plus x = 1
    print(total + 1)


if __name__ == "__main__":
    main()
