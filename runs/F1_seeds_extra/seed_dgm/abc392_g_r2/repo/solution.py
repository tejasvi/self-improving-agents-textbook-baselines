import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = [int(x) for x in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(s)
    W = 7  # slot width in decimal digits; coefficients <= 1e6 < 1e7
    L = M + 1
    # Decimal string, most significant digit first: slot k is at position L-1-k from the right.
    buf = bytearray(b"0" * (W * L))
    for v in s:
        # slot v ends at index W*(L-1-v) + W-1 in the string (least-significant digit)
        buf[W * (L - 1 - v) + W - 1] = 49  # '1'
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    x = Decimal(buf.decode())
    p = ctx.multiply(x, x)
    t = format(p, "f")  # plain digits, no exponent
    # pad so the total length is a multiple of W and covers all slots
    total_slots = 2 * L
    t = t.rjust(W * total_slots, "0")
    ln = len(t)
    total = 0
    for v in s:
        k = 2 * v  # coefficient index (sum of two elements)
        end = ln - W * k
        total += int(t[end - W:end])
    total -= n
    print(total // 2)


main()
