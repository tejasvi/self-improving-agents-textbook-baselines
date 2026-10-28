import sys
import decimal


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = [int(x) for x in data[1:1 + n]]
    V = max(S)
    present = bytearray(V + 1)
    for s in S:
        present[s] = 1

    W = 7  # decimal digits per slot; coefficients <= N <= 10^6 < 10^7
    # Build big-endian decimal string: slot V first (most significant) ... slot 0 last
    one = "0" * (W - 1) + "1"
    parts = [one if present[v] else "0" * W for v in range(V, -1, -1)]
    text = "".join(parts)
    ctx = decimal.Context(prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX,
                          Emin=decimal.MIN_EMIN, traps=[])
    X = decimal.Decimal(text)
    P = ctx.multiply(X, X)
    ptxt = format(P, "f")
    total_slots = 2 * V + 1
    ptxt = ptxt.rjust(total_slots * W, "0")
    L = len(ptxt)

    def coef(s):
        # slot s corresponds to position from left: (2V - s) * W
        pos = L - (s + 1) * W
        return int(ptxt[pos:pos + W])

    ans = 0
    for b in S:
        c = coef(2 * b)
        if present[b]:  # A = C = B self pair
            c -= 1
        ans += c // 2
    sys.stdout.write(str(ans) + "\n")


main()
