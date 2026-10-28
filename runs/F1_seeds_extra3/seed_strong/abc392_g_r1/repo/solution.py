import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    M = max(S)
    W = 7  # decimal digits per block; coefficients <= 10^6 < 10^7
    nb = M + 1
    L = W * nb
    # indicator packed into decimal digits: block i (value i) occupies
    # string positions [L - W*(i+1), L - W*i); its last char is the units digit.
    arr = bytearray(b'0' * L)
    for x in S:
        arr[L - W * x - 1] = ord('1')
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    d = Decimal(arr.decode())
    r = ctx.multiply(d, d)
    rs = str(r)
    total_len = W * (2 * M + 1)
    if len(rs) < total_len:
        rs = rs.zfill(total_len)
    Lr = total_len
    ans = 0
    for b in S:
        s = 2 * b
        c = int(rs[Lr - W * (s + 1): Lr - W * s])
        ans += (c - 1) // 2
    print(ans)


main()
