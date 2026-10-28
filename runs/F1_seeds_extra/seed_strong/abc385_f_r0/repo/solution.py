import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1::2][:n]]
    hs = [int(v) for v in data[2::2][:n]]
    # maximum threshold as exact fraction bn/bd (bd > 0)
    best_num = None
    best_den = 1
    for j in range(n - 1):
        x0, h0 = xs[j], hs[j]
        x1, h1 = xs[j + 1], hs[j + 1]
        num = h0 * x1 - h1 * x0
        den = x1 - x0
        if best_num is None or num * best_den > best_num * den:
            best_num, best_den = num, den
    if best_num is None or best_num < 0:
        print(-1)
        return
    # exact decimal output with 18 digits
    scale = 10 ** 18
    q = best_num * scale // best_den
    rem = best_num * scale - q * best_den
    ip = q // scale
    fp = q % scale
    # rounding to nearest
    if 2 * rem >= best_den:
        fp += 1
        if fp == scale:
            fp = 0
            ip += 1
    print(f"{ip}.{fp:018d}")


main()
