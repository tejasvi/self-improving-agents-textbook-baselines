import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    hs = [int(data[2 + 2 * i]) for i in range(n)]
    # Max over adjacent pairs of the y-intercept at x=0 of the line through them.
    # Stored as exact fraction bn/bd with bd > 0.
    bn = None
    bd = 1
    for k in range(n - 1):
        x1, h1 = xs[k], hs[k]
        x2, h2 = xs[k + 1], hs[k + 1]
        num = h1 * x2 - h2 * x1
        den = x2 - x1
        if bn is None or num * bd > bn * den:
            bn, bd = num, den
    if bn is None or bn < 0:
        print(-1)
        return
    # bn >= 0 here
    q, r = divmod(bn * 10**18, bd)
    # Exact decimal with 18 fractional digits (rounded down; error < 1e-18)
    print(f"{q // 10**18}.{q % 10**18:018d}")


main()
