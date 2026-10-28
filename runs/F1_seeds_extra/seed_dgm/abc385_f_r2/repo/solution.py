import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1:1 + 2 * n:2]]
    hs = [int(v) for v in data[2:2 + 2 * n:2]]
    # Best fraction bn/bd (bd > 0), exact comparison via cross-multiplication.
    have = False
    bn, bd = 0, 1
    for i in range(1, n):
        x0, h0 = xs[i - 1], hs[i - 1]
        x1, h1 = xs[i], hs[i]
        num = x1 * h0 - x0 * h1
        den = x1 - x0
        if not have or num * bd > bn * den:
            bn, bd = num, den
            have = True
    if not have or bn < 0:
        print(-1)
    else:
        print("%.18f" % (bn / bd))


main()
