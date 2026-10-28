import sys
from decimal import Decimal, getcontext, MAX_PREC, MAX_EMAX


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    if n < 3:
        print(0)
        return
    M = max(S)
    W = 7  # digits per slot; coefficients <= N <= 10^6 fit in 7 digits
    present = bytearray(M + 1)
    for x in S:
        present[x] = 1
    # Build decimal string, most significant slot first (slot index M down to 0).
    # Each slot is W digits: six '0's followed by the bit.
    pad = "000000"
    parts = [pad + ("1" if present[x] else "0") for x in range(M, -1, -1)]
    s_in = "".join(parts)
    ctx = getcontext()
    ctx.prec = MAX_PREC
    ctx.Emax = MAX_EMAX
    ctx.Emin = -MAX_EMAX
    d = Decimal(s_in)
    sq = d * d
    text = format(sq, "f")
    L = (2 * M + 1) * W
    if len(text) < L:
        text = "0" * (L - len(text)) + text
    # slot for coefficient index s occupies digits at positions
    # [L - W*(s+1), L - W*s) counted from the left of text.
    total = 0
    for b in S:
        s = 2 * b
        if s > 2 * M:
            continue
        hi = L - W * s
        total += int(text[hi - W:hi])
    # P(s) counts ordered pairs (a,c) incl. a==c (only when s even and a=b).
    # Subtract the a==c term: b in S gives one such pair for s=2b.
    total -= n
    # Each unordered pair a<c counted twice in ordered count.
    total //= 2
    print(total)


main()
