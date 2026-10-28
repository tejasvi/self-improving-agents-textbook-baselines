import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    sx, sy = int(data[2]), int(data[3])
    p = 4
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(data[p]); ys[i] = int(data[p + 1]); p += 2

    LIM = 10**9
    OFF = LIM
    SH = 1 << 32
    # row structure: key = (y+OFF)*SH + (x+OFF), sorted
    rkey = [((ys[i] + OFF) * SH) + (xs[i] + OFF) for i in range(n)]
    rord = sorted(range(n), key=lambda i: rkey[i])
    rkeys = [rkey[i] for i in rord]
    rpos = [0] * n
    for idx, i in enumerate(rord):
        rpos[i] = idx
    # column structure: key = (x+OFF)*SH + (y+OFF), sorted
    ckey = [((xs[i] + OFF) * SH) + (ys[i] + OFF) for i in range(n)]
    cord = sorted(range(n), key=lambda i: ckey[i])
    ckeys = [ckey[i] for i in cord]
    cpos = [0] * n
    for idx, i in enumerate(cord):
        cpos[i] = idx

    rpar = list(range(n + 1))
    cpar = list(range(n + 1))

    def find(par, x):
        r = x
        while par[r] != r:
            r = par[r]
        while par[x] != r:
            par[x], x = r, par[x]
        return r

    x, y = sx, sy
    count = 0

    def kill(h):
        rpar[rpos[h]] = rpos[h] + 1
        cpar[cpos[h]] = cpos[h] + 1

    for _ in range(m):
        d = data[p].decode()
        c = int(data[p + 1]); p += 2
        if d == 'L' or d == 'R':
            if d == 'R':
                nx = x + c
                lo, hi = x, nx
            else:
                nx = x - c
                lo, hi = nx, x
            if -LIM <= y <= LIM:
                lo_c = max(lo, -LIM); hi_c = min(hi, LIM)
                if lo_c <= hi_c:
                    base = (y + OFF) * SH + OFF
                    a = bisect_left(rkeys, base + lo_c + 0)
                    b = bisect_right(rkeys, base + hi_c)
                    i = find(rpar, a)
                    while i < b:
                        h = rord[i]
                        kill(h)
                        count += 1
                        i = find(rpar, i + 1)
            x = nx
        else:
            if d == 'U':
                ny = y + c
                lo, hi = y, ny
            else:
                ny = y - c
                lo, hi = ny, y
            if -LIM <= x <= LIM:
                lo_c = max(lo, -LIM); hi_c = min(hi, LIM)
                if lo_c <= hi_c:
                    base = (x + OFF) * SH + OFF
                    a = bisect_left(ckeys, base + lo_c)
                    b = bisect_right(ckeys, base + hi_c)
                    i = find(cpar, a)
                    while i < b:
                        h = cord[i]
                        kill(h)
                        count += 1
                        i = find(cpar, i + 1)
            y = ny

    print(x, y, count)


main()
