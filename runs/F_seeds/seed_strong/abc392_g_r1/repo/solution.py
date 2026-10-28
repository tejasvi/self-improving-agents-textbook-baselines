import sys
from decimal import Decimal, Context

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = [int(x) for x in data[1:1 + n]]
    M = max(s)
    # indicator in base 10^7 blocks, most significant block first (block index M down to 0)
    ind = bytearray(b'0' * (7 * (M + 1)))
    # position of block v in string: chars [7*(M-v), 7*(M-v)+7)
    # set last digit of each block to '1' for members
    for v in s:
        ind[7 * (M - v) + 6] = 49  # '1'
    X = Decimal(ind.decode())
    L = 7 * (M + 1)
    ctx = Context(prec=2 * L + 10, Emax=10**9, Emin=-10**9)
    P = ctx.multiply(X, X)
    t = str(P)
    total_blocks = 2 * M + 1
    t = t.zfill(7 * total_blocks)
    T = len(t)
    total = 0
    for b in s:
        k = 2 * b  # block index k -> chars [T-7(k+1), T-7k)
        end = T - 7 * k
        total += int(t[end - 7:end])
    print((total - n) // 2)

main()
