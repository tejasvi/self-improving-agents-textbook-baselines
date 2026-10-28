import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = list(map(int, data[1:1 + n]))
    M = max(s)
    inS = bytearray(M + 1)
    for x in s:
        inS[x] = 1

    # Polynomial P(z) = sum_{x in S} z^x. Compute P(z)^2 via decimal
    # multiplication with base 10^W slots (coefficients <= n < 10^W).
    W = 7
    blocks = ['0000001' if inS[i] else '0000000' for i in range(M, -1, -1)]
    num_str = ''.join(blocks)
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    d = Decimal(num_str)
    prod = ctx.multiply(d, d)
    t = format(prod, 'f')
    L = W * (2 * M + 1)
    if len(t) < L:
        t = '0' * (L - len(t)) + t
    # t is big-endian; slot k (coefficient of z^k) is t[L-W*(k+1) : L-W*k]
    total = 0
    for x in s:
        k = 2 * x
        lo = L - W * (k + 1)
        c = int(t[lo:lo + W])
        total += (c - 1) // 2
    print(total)


main()
