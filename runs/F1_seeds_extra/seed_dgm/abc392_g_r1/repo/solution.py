import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(S)
    W = 7  # decimal digits per slot; counts are <= 1e6 so no overflow
    # Indicator polynomial: slot v holds 1 if v in S. Most significant slot first.
    buf = bytearray(b'0' * (W * (M + 1)))
    for s in S:
        buf[(M - s) * W + W - 1] = ord('1')
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    X = ctx.create_decimal(buf.decode())
    P = ctx.multiply(X, X)
    T = W * (2 * M + 1)
    res = format(P, 'f')
    res = res.zfill(T)
    L = len(res)
    total = 0
    for b in S:
        # slot 2b, counted from the least significant end
        hi = L - W * (2 * b)
        lo = hi - W
        c = int(res[lo:hi])
        total += (c - 1) // 2
    print(total)


main()
