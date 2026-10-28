import sys
from decimal import Decimal, Context, MAX_PREC, ROUND_FLOOR


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(v) for v in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(S)
    W = 7  # decimal digits per slot; coefficients <= 1e6 < 10^7
    # Build x(t) = sum_{s in S} t^s with t = 10^W, as a decimal string (MSB first).
    # Slot s is at position (M - s) from the top.
    L = M + 1
    buf = bytearray(b"0" * (L * W))
    for s in S:
        # slot index from the most significant side
        pos = (M - s) * W
        buf[pos + W - 1] = ord("1")
    # Square using Decimal (libmpdec uses NTT for large multiplication)
    ctx = Context(prec=MAX_PREC, Emax=MAX_PREC, Emin=-MAX_PREC, rounding=ROUND_FLOOR)
    x = Decimal(buf.decode())
    sq = ctx.multiply(x, x)
    t = str(sq.to_integral_value(context=ctx))
    # Pad to full length of square: 2M+1 slots
    total_slots = 2 * M + 1
    t = t.rjust(total_slots * W, "0")
    # slot for exponent e is at index (2M - e) from the left
    ans2 = 0
    for b in S:
        e = 2 * b
        idx = (2 * M - e) * W
        r = int(t[idx:idx + W])
        ans2 += r - 1
    print(ans2 // 2)


main()
