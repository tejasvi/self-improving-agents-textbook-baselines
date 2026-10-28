import sys
import decimal


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    M = max(S)
    W = 7  # digits per slot; coefficients of P^2 are <= N <= 1e6 < 10^7
    L_in = W * (M + 1)
    buf = bytearray(b'0' * L_in)
    for s in S:
        buf[L_in - 1 - W * s] = ord('1')
    ctx = decimal.Context(prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX,
                          Emin=decimal.MIN_EMIN)
    x = decimal.Decimal(buf.decode())
    sq = ctx.multiply(x, x)
    L2 = W * (2 * M + 1)
    r = format(sq, 'f')
    if len(r) < L2:
        r = r.rjust(L2, '0')
    total = 0
    for b in S:
        hi = L2 - W * 2 * b
        total += int(r[hi - W:hi]) - 1  # remove diagonal a == c == b
    print(total // 2)


main()
