import sys
from decimal import Decimal, localcontext, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(S)
    W = 7  # decimal digits per slot; coefficients <= 1e6 fit in 7 digits
    L = W * (M + 1)
    # buf[i] is the decimal digit at power 10^(W*x) where x = (L-1-i)//W ... build big-endian
    buf = bytearray(b'0' * L)
    # slot x (value 10^(W*x)) occupies string indices [L-W*(x+1), L-W*x)
    # its least significant digit is at index L-W*x-1
    for x in S:
        buf[L - W * x - 1] = ord('1')
    poly = Decimal(buf.decode())
    with localcontext() as ctx:
        ctx.prec = MAX_PREC
        ctx.Emax = MAX_EMAX
        ctx.Emin = MIN_EMIN
        sq = poly * poly
    s = format(sq, 'f')
    # s is the full integer decimal string; pad to get slots
    total_len = W * (2 * M + 1)
    if len(s) < total_len:
        s = '0' * (total_len - len(s)) + s
    Ls = len(s)
    ans = 0
    for b in S:
        x = 2 * b
        # slot x: string indices [Ls-W*(x+1), Ls-W*x)
        c = int(s[Ls - W * (x + 1): Ls - W * x])
        ans += (c - 1) // 2
    print(ans)


main()
