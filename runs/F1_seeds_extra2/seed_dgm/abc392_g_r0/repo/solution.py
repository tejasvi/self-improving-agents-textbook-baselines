import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    M = max(S)
    W = 7  # coefficients <= N <= 10^6 fit in 7 decimal digits
    # Polynomial P(x) = sum x^s, evaluated at x = 10^W (Kronecker substitution).
    L = W * (M + 1)
    buf = bytearray(b'0' * L)
    for s in S:
        buf[L - 1 - W * s] = ord('1')
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    p = Decimal(buf.decode())
    sq = ctx.multiply(p, p)
    # Convert result to string, reversed so block v is at [W*v, W*v+W)
    t = format(sq, 'f')
    total_blocks = 2 * M + 1
    t = t.zfill(W * total_blocks)
    rs = t[::-1]
    ans2 = 0  # sum of (conv[2B] - 1) over B in S
    for b in S:
        v = 2 * b
        ans2 += int(rs[W * v:W * v + W][::-1]) - 1
    print(ans2 // 2)


main()
