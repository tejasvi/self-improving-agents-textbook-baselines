import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    sx = int(data[2]); sy = int(data[3])
    xs = [0] * n
    ys = [0] * n
    p = 4
    for i in range(n):
        xs[i] = int(data[p]); ys[i] = int(data[p + 1]); p += 2
    INF = float('inf')

    # Row structure: sorted by (y, x), sentinel after each row block.
    order = sorted(range(n), key=lambda i: (ys[i], xs[i]))
    rowX = []
    rowH = []
    rowPos = [0] * n
    rowRange = {}
    i = 0
    while i < n:
        y = ys[order[i]]
        start = len(rowX)
        while i < n and ys[order[i]] == y:
            h = order[i]
            rowPos[h] = len(rowX)
            rowX.append(xs[h]); rowH.append(h)
            i += 1
        rowRange[y] = (start, len(rowX))
        rowX.append(INF); rowH.append(-1)
    R = len(rowX)
    rowNxt = list(range(R + 1))

    # Column structure: sorted by (x, y), sentinel after each block.
    order = sorted(range(n), key=lambda i: (xs[i], ys[i]))
    colY = []
    colH = []
    colPos = [0] * n
    colRange = {}
    i = 0
    while i < n:
        x = xs[order[i]]
        start = len(colY)
        while i < n and xs[order[i]] == x:
            h = order[i]
            colPos[h] = len(colY)
            colY.append(ys[h]); colH.append(h)
            i += 1
        colRange[x] = (start, len(colY))
        colY.append(INF); colH.append(-1)
    C = len(colY)
    colNxt = list(range(C + 1))

    def find(nxt, i):
        r = i
        while nxt[r] != r:
            r = nxt[r]
        while nxt[i] != r:
            nxt[i], i = r, nxt[i]
        return r

    # Shared removal logic.
    count = 0
    cx, cy = sx, sy
    for _ in range(m):
        d = data[p]; c = int(data[p + 1]); p += 2
        if d == b'U' or d == b'D':
            ny = cy + c if d == b'U' else cy - c
            x = cx
            lo, hi = (cy, ny) if cy <= ny else (ny, cy)
            rr = colRange.get(x)
            if rr is not None:
                s, e = rr
                j = find(colNxt, bisect_left(colY, lo, s, e))
                while j < e and colY[j] <= hi:
                    h = colH[j]
                    count += 1
                    colNxt[j] = j + 1
                    rp = rowPos[h]
                    rowNxt[rp] = rp + 1
                    j = find(colNxt, j + 1)
            cy = ny
        else:
            nx = cx + c if d == b'R' else cx - c
            y = cy
            lo, hi = (cx, nx) if cx <= nx else (nx, cx)
            rr = rowRange.get(y)
            if rr is not None:
                s, e = rr
                j = find(rowNxt, bisect_left(rowX, lo, s, e))
                while j < e and rowX[j] <= hi:
                    h = rowH[j]
                    count += 1
                    rowNxt[j] = j + 1
                    cp = colPos[h]
                    colNxt[cp] = cp + 1
                    j = find(rowNxt, j + 1)
            cx = nx
    print(cx, cy, count)


main()
