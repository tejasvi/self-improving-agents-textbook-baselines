import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(S)
    # Coefficients of self-convolution are <= n <= 1e6 < 10^7, so use 7 decimal digits per slot.
    W = 7
    present = bytearray(b'0' * (M + 1))
    for s in S:
        present[s] = ord('1')
    zero_block = b'0' * (W - 1)
    buf = bytearray()
    for p in range(M, -1, -1):
        buf += zero_block
        buf.append(present[p])
    s_str = buf.decode()
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=-MAX_EMAX)
    X = Decimal(s_str)
    R = ctx.multiply(X, X)
    rs = format(R, 'f')
    total_blocks = 2 * M + 1
    rs = rs.rjust(total_blocks * W, '0')
    L = len(rs)
    ans2 = 0  # sum over B in S of (r(2B) - 1)
    for b in S:
        s = 2 * b
        # block index from right is s
        end = L - W * s
        start = end - W
        r = int(rs[start:end])
        ans2 += r - 1
    print(ans2 // 2)  # r(2B)-1 counts ordered pairs a!=c, so unordered = (r-1)/2


main()
