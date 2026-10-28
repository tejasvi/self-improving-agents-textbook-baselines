import sys
import decimal


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = list(map(int, data[1:1 + n]))
    V = max(s)
    W = 7  # digits per slot; coefficients <= N <= 1e6 < 10^7, no carries
    # Chunk i (from left) holds value V - i.
    ind = bytearray(b'0' * (W * (V + 1)))
    for x in s:
        # chunk index i = V - x; its last digit (units) is at offset i*W + W-1
        ind[(V - x) * W + W - 1] = ord('1')
    # Use the string as an integer in base 10: chunk i, digit position in string.
    A = decimal.Decimal(ind.decode())
    L = 2 * W * (V + 1) + 10
    ctx = decimal.Context(prec=L + 10, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN)
    P = ctx.multiply(A, A)
    t = format(P, 'f')
    total_chunks = 2 * V + 1
    t = t.rjust(W * total_chunks, '0')
    # chunk j from left corresponds to sum-value T = 2V - j
    ans2 = 0
    for x in s:
        j = 2 * V - 2 * x
        c = int(t[j * W:(j + 1) * W])
        ans2 += c - 1
    print(ans2 // 2)


main()
