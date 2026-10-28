import sys
from decimal import Decimal, localcontext, MAX_PREC, MAX_EMAX


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    M = max(S)
    present = bytearray(M + 1)
    for v in S:
        present[v] = 1

    # Pack indicator a[i] (i in 0..M) into decimal digits, 7 digits per slot,
    # most significant slot first. Autoconvolution coefficients <= 1e6 < 1e7.
    W = 7
    zero = "0" * W
    one = "0" * (W - 1) + "1"
    # build list of blocks from highest index to lowest
    blocks = [one if present[i] else zero for i in range(M, -1, -1)]
    s_in = "".join(blocks)
    total_slots = 2 * M + 1
    T = W * total_slots
    prec = 2 * T + 10

    with localcontext() as ctx:
        ctx.prec = prec
        ctx.Emax = MAX_EMAX
        ctx.Emin = -MAX_EMAX
        d = Decimal(s_in)
        p = d * d
        ps = format(p, "f")

    # Strip possible decimal point / exponent artifacts (integer result expected)
    if "." in ps:
        ps = ps.split(".")[0]
    ps = ps.zfill(T)
    ans2 = 0  # sum over B of (r(2B) - 1)
    for b in S:
        s = 2 * b
        # slot s occupies ps[T - W*(s+1) : T - W*s]
        r = int(ps[T - W * (s + 1): T - W * s])
        ans2 += r - 1
    print(ans2 // 2)


main()
