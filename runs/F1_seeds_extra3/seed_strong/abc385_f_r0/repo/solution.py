import sys
from decimal import Decimal, getcontext


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1::2][:n]]
    hs = [int(v) for v in data[2::2][:n]]
    # Maximum over adjacent pairs of the intercept at x=0 of the line through
    # consecutive buildings: num/den with den > 0.
    bnum, bden = None, 1
    for i in range(1, n):
        den = xs[i] - xs[i - 1]
        num = hs[i - 1] * xs[i] - hs[i] * xs[i - 1]
        if bnum is None or num * bden > bnum * den:
            bnum, bden = num, den
    if bnum is None or bnum < 0:
        print(-1)
        return
    getcontext().prec = 60
    q = Decimal(bnum) / Decimal(bden)
    print(format(q, ".18f"))


main()
