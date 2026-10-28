import sys


def iroot(n, k):
    # largest r with r**k <= n, exact integer arithmetic
    if k == 1:
        return n
    r = int(round(n ** (1.0 / k)))
    while r > 0 and r ** k > n:
        r -= 1
    while (r + 1) ** k <= n:
        r += 1
    return r


def mobius_upto(m):
    mu = [1] * (m + 1)
    is_p = [True] * (m + 1)
    for p in range(2, m + 1):
        if is_p[p]:
            for q in range(p, m + 1, p):
                if q > p:
                    is_p[q] = False
                mu[q] = -mu[q]
            for q in range(p * p, m + 1, p * p):
                mu[q] = 0
    return mu


def solve(n):
    # count perfect powers x in [2, n] via inclusion-exclusion over exponents
    if n < 1:
        return 0
    K = n.bit_length()  # 2^K > n, so exponents >= K give only root 1
    mu = mobius_upto(max(K, 2))
    total = 0
    for k in range(2, K + 1):
        if mu[k] == 0:
            continue
        total += -mu[k] * (iroot(n, k) - 1)
    return total + 1  # plus the number 1


def main():
    n = int(sys.stdin.read().split()[0])
    print(solve(n))


if __name__ == "__main__":
    main()
