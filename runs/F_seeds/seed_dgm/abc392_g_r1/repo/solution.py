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
    L = 2 * M + 1          # slots for sums 0..2M
    W = 7                  # decimal digits per slot (counts <= 10^6 < 10^7)
    total = L * W
    buf = bytearray(b'0' * total)
    # slot a stored at digit positions [a*W, a*W+W) counted from least significant;
    # in the string (most significant first) that is index total-1-(a*W+W-1)
    for a in S:
        buf[total - 1 - a * W] = ord('1')
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    x = Decimal(buf.decode())
    sq = ctx.multiply(x, x)
    s = format(sq, 'f')
    # s is the integer string; pad to full length
    if len(s) < total:
        s = '0' * (total - len(s)) + s
    # slot for sum t is at string index total-1-(t*W+W-1) .. total-1-t*W
    ans = 0
    for b in S:
        t = 2 * b
        start = total - (t + 1) * W
        f = int(s[start:start + W])
        ans += (f - 1) // 2
    print(ans)


main()
