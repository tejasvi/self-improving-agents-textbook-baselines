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
    present = bytearray(M + 1)
    for s in S:
        present[s] = 1
    # Big-endian packing: value v occupies slot (M - v), 7 decimal digits each.
    on = b'0000001'
    off = b'0000000'
    parts = [on if present[v] else off for v in range(M, -1, -1)]
    text = b''.join(parts).decode()
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    X = Decimal(text)
    P = ctx.multiply(X, X)
    ps = format(P, 'f')
    L = 7 * (2 * M + 1)
    if len(ps) < L:
        ps = '0' * (L - len(ps)) + ps
    # Coefficient of sum t sits at slot (2M - t): digits [(2M - t)*7, +7)
    total = 0
    for b in S:
        t = 2 * b
        pos = (2 * M - t) * 7
        c = int(ps[pos:pos + 7])
        total += (c - 1) // 2
    print(total)


main()
