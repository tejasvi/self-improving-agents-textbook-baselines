import sys
from decimal import Context, MAX_PREC, MAX_EMAX, MIN_EMIN
def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    M = max(S)
    W = 7
    arr = bytearray(b'0' * (W * (M + 1)))
    for s in S:
        arr[(M - s) * W + W - 1] = 49
    X = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN).create_decimal(arr.decode())
    Y = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN).multiply(X, X)
    r = format(Y, 'f')
    T = (2 * M + 1) * W
    r = r.rjust(T, '0')
    L = len(r)
    total = 0
    for b in S:
        end = L - 2 * b * W
        c = int(r[end - W:end])
        total += (c - 1) >> 1
    print(total)
main()
