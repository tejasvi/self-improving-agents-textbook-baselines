import sys
import decimal


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = [int(x) for x in data[1:1 + n]]
    M = max(s)
    W = 7  # slot width in decimal digits; counts <= 10^6 < 10^7
    total = 2 * M + 1  # slots for convolution indices 0..2M

    # Build X = sum_{v in S} 10^{W*v}, slot v stored with v-th slot from the right.
    L = W * (M + 1)
    buf = bytearray(b'0' * L)
    for v in s:
        # least significant digit of slot v (from the left index)
        buf[W * (M - v) + W - 1] = ord('1')
    ctx = decimal.Context(prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX,
                          Emin=decimal.MIN_EMIN)
    X = decimal.Decimal(buf.decode())
    P = ctx.multiply(X, X)
    t = str(P)
    Ltot = W * total
    t = t.rjust(Ltot, '0')
    # slot index s occupies t[Ltot - W*(idx+1) : Ltot - W*idx]
    ans2 = 0
    for v in s:
        idx = 2 * v
        start = Ltot - W * (idx + 1)
        ans2 += int(t[start:start + W]) - 1
    print(ans2 // 2)


main()
