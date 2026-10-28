import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, setcontext


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(S)
    W = 7  # each coefficient <= N <= 10^6 < 10^7, so 7 decimal digits suffice
    L = W * (M + 1)
    # buf[k] for block index: block for value x occupies digit positions
    # [W*(M-x), W*(M-x)+W) from the left; its units digit is at W*(M-x)+W-1.
    buf = bytearray(b'0' * L)
    for x in S:
        buf[W * (M - x) + W - 1] = ord('1')
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=-MAX_EMAX)
    setcontext(ctx)
    a = Decimal(buf.decode())
    p = a * a
    res = str(p)
    total_len = W * (2 * M + 1)
    # pad to total_len (res has no leading zeros, so left-pad)
    if len(res) < total_len:
        res = '0' * (total_len - len(res)) + res
    ans = 0
    for m in S:
        s = 2 * m
        off = W * (2 * M - s)
        c = int(res[off:off + W])
        ans += (c - 1) // 2
    print(ans)


main()
