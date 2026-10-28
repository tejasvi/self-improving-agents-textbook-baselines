import sys
from decimal import Decimal, Context, MAX_PREC, MAX_EMAX, MIN_EMIN


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    M = max(S)
    W = 7  # decimal digits per slot; coefficients <= 1e6 < 10^7
    # Build polynomial P(x) = sum x^s for s in S, packed base 10^W, most significant first.
    present = bytearray(M + 1)
    for s in S:
        present[s] = 1
    # slot v -> chunk of W digits with last digit = present[v]
    pad = b"000000"
    chunks = []
    for v in range(M, -1, -1):
        chunks.append(pad + (b"1" if present[v] else b"0"))
    num_str = b"".join(chunks).decode()
    ctx = Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN)
    D = Decimal(num_str)
    sq = ctx.multiply(D, D)
    res = str(sq)
    # Slots of the product: indices 0..2M
    L = len(res)
    total_slots = 2 * M + 1
    need = total_slots * W
    if L < need:
        res = "0" * (need - L) + res
    # res digits: most significant slot first, slot 2M first.
    # Extract f(2B) for B in S.
    ans2 = 0
    for B in S:
        s = 2 * B
        # slot s is at position (2M - s) from the left
        p = (2 * M - s) * W
        f = int(res[p:p + W])
        ans2 += f - 1
    print(ans2 // 2)


main()
