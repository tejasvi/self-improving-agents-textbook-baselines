import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1])
    sx = int(data[idx + 2]); sy = int(data[idx + 3])
    idx += 4
    X = [0] * n
    Y = [0] * n
    for i in range(n):
        X[i] = int(data[idx]); Y[i] = int(data[idx + 1])
        idx += 2

    OFF = 2 * 10**9 + 5
    BIG = 5 * 10**9 + 11

    def enc(a, b):
        return (a + OFF) * BIG + (b + OFF)

    # Column ordering: sorted by (x, y)
    ordA = sorted(range(n), key=lambda i: (X[i], Y[i]))
    keysA = [enc(X[i], Y[i]) for i in ordA]
    posA = [0] * n
    for p, i in enumerate(ordA):
        posA[i] = p
    # Row ordering: sorted by (y, x)
    ordB = sorted(range(n), key=lambda i: (Y[i], X[i]))
    keysB = [enc(Y[i], X[i]) for i in ordB]
    posB = [0] * n
    for p, i in enumerate(ordB):
        posB[i] = p

    parA = list(range(n + 1))
    parB = list(range(n + 1))

    def find(par, x):
        root = x
        while par[root] != root:
            root = par[root]
        while par[x] != root:
            par[x], x = root, par[x]
        return root

    removed = [False] * n
    count = 0

    def remove(i):
        removed[i] = True
        pa = posA[i]
        parA[pa] = pa + 1
        pb = posB[i]
        parB[pb] = pb + 1

    def sweep(keys, par, ordr, lo_key, hi_key):
        # collect unremoved houses with lo_key <= key <= hi_key
        nonlocal count
        p = find(par, bisect_left(keys, lo_key))
        L = len(keys)
        while p < L and keys[p] <= hi_key:
            i = ordr[p]
            # the house is unremoved (find guarantees it)
            remove(i)
            count += 1
            p = find(par, p + 1)

    x, y = sx, sy
    for _ in range(m):
        d = data[idx].decode()
        c = int(data[idx + 1])
        idx += 2
        if d == 'U' or d == 'D':
            if d == 'U':
                ny = y + c; lo, hi = y, ny
            else:
                ny = y - c; lo, hi = ny, y
            # vertical sweep on column x
            sweep(keysA, parA, ordA, enc(x, lo), enc(x, hi))
            y = ny
        else:
            if d == 'R':
                nx = x + c; lo, hi = x, nx
            else:
                nx = x - c; lo, hi = nx, x
            # horizontal sweep on row y
            sweep(keysB, parB, ordB, enc(y, lo), enc(y, hi))
            x = nx

    print(x, y, count)


main()
