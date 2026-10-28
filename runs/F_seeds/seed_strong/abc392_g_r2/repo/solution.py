import sys
from decimal import Decimal, localcontext, MAX_PREC, MAX_EMAX


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    M = max(S)
    W = 7  # decimal digits per slot; counts <= 1e6 < 10^7
    L = W * (M + 1)
    arr = bytearray(b'0') * L
    for s in S:
        arr[L - 1 - W * s] = 49  # '1'
    with localcontext() as ctx:
        ctx.prec = MAX_PREC
        ctx.Emax = MAX_EMAX
        ctx.Emin = -MAX_EMAX
        X = Decimal(arr.decode())
        Y = X * X
        t = str(Y)
    Lp = W * (2 * M + 2)
    if len(t) < Lp:
        t = '0' * (Lp - len(t)) + t
    total = 0
    for b in S:
        k = 2 * b
        hi = Lp - W * k
        total += int(t[hi - W:hi])
    print((total - n) // 2)


main()
