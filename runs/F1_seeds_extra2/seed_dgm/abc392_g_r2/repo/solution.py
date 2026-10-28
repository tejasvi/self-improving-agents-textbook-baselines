import sys
from decimal import Decimal, getcontext, MAX_PREC, MAX_EMAX


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = [int(x) for x in data[1:1 + n]]
    M = max(s)
    L = 2 * M + 1  # coefficient indices 0..2M
    W = 7  # each coefficient <= 1e6 < 10^7 fits in 7 decimal digits
    present = bytearray(M + 1)
    for x in s:
        present[x] = 1
    # Build polynomial string, most significant coefficient first.
    zero = '0' * W
    one = '0' * (W - 1) + '1'
    parts = []
    # index 0 is least significant -> appended last
    for i in range(L - 1, -1, -1):
        parts.append(one if (i <= M and present[i]) else zero)
    # The digit string for polynomial p(10^W) where coefficients a_i.
    # Avoid leading-zero issues: Decimal handles them.
    txt = ''.join(parts)
    ctx = getcontext()
    ctx.prec = MAX_PREC
    ctx.Emax = MAX_EMAX
    ctx.Emin = -MAX_EMAX
    ctx.traps[__import__('decimal').Inexact] = False
    D = Decimal(txt)
    R = D * D
    rs = format(R, 'f')
    total_len = W * (2 * L - 1)
    rs = rs.zfill(total_len)
    Lr = len(rs)
    ans = 0
    for b in s:
        i = 2 * b
        # coefficient at index i: slot counted from the right
        end = Lr - W * i
        c = int(rs[end - W:end])
        ans += (c - 1) // 2
    print(ans)


main()
