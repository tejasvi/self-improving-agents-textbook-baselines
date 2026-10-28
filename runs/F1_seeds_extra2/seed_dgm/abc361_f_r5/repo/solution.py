import sys


def iroot(n, k):
    """Largest integer r with r**k <= n."""
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


def solve(n):
    if n < 1:
        return 0
    # count of perfect powers in [2, n] via Mobius inversion
    total = 0
    for k in range(2, n.bit_length() + 2):
        r = iroot(n, k)
        if r < 2:
            break
        total -= mobius(k) * (r - 1)
    return total + 1  # plus x = 1


def main():
    n = int(sys.stdin.read().split()[0])
    print(solve(n))


if __name__ == "__main__":
    main()
