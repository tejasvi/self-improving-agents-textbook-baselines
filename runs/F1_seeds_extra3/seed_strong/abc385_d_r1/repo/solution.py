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
        X[i] = int(data[idx]); Y[i] = int(data[idx + 1]); idx += 2

    # Row structure: group by y, sorted by x. Global arrays with sentinel after each group.
    order_r = sorted(range(n), key=lambda i: (Y[i], X[i]))
    RX = []  # x values in global order (sentinels get a dummy value)
    RH = []  # house id or -1 for sentinel
    row_group = {}  # y -> (start, end)
    i = 0
    while i < n:
        y = Y[order_r[i]]
        j = i
        start = len(RX)
        while j < n and Y[order_r[j]] == y:
            h = order_r[j]
            RX.append(X[h]); RH.append(h)
            j += 1
        row_group[y] = (start, len(RX))
        RX.append(0); RH.append(-1)  # sentinel
        i = j
    TR = len(RX)
    rpos = [0] * n
    for p in range(TR):
        if RH[p] >= 0:
            rpos[RH[p]] = p
    rnxt = list(range(TR + 1))

    # Column structure: group by x, sorted by y.
    order_c = sorted(range(n), key=lambda i: (X[i], Y[i]))
    CY = []
    CH = []
    col_group = {}
    i = 0
    while i < n:
        x = X[order_c[i]]
        j = i
        start = len(CY)
        while j < n and X[order_c[j]] == x:
            h = order_c[j]
            CY.append(Y[h]); CH.append(h)
            j += 1
        col_group[x] = (start, len(CY))
        CY.append(0); CH.append(-1)
        i = j
    TC = len(CY)
    cpos = [0] * n
    for p in range(TC):
        if CH[p] >= 0:
            cpos[CH[p]] = p
    cnxt = list(range(TC + 1))

    def find(par, a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    visited = [False] * n
    count = 0

    def visit_row_range(y, a, b):
        nonlocal count
        g = row_group.get(y)
        if g is None:
            return
        s, e = g
        p = bisect_left(RX, a, s, e)
        q = find(rnxt, p)
        while q < e and RX[q] <= b:
            h = RH[q]
            rnxt[q] = q + 1
            if not visited[h]:
                visited[h] = True
                count += 1
                cp = cpos[h]
                cnxt[cp] = cp + 1
            q = find(rnxt, q + 1)

    def visit_col_range(x, a, b):
        nonlocal count
        g = col_group.get(x)
        if g is None:
            return
        s, e = g
        p = bisect_left(CY, a, s, e)
        q = find(cnxt, p)
        while q < e and CY[q] <= b:
            h = CH[q]
            cnxt[q] = q + 1
            if not visited[h]:
                visited[h] = True
                count += 1
                rp = rpos[h]
                rnxt[rp] = rp + 1
            q = find(cnxt, q + 1)

    x, y = sx, sy
    pos = 4 + 2 * n
    for _ in range(m):
        d = data[pos]
        c = int(data[pos + 1])
        pos += 2
        if d == b'U':
            visit_col_range(x, y, y + c)
            y += c
        elif d == b'D':
            visit_col_range(x, y - c, y)
            y -= c
        elif d == b'L':
            visit_row_range(y, x - c, x)
            x -= c
        else:
            visit_row_range(y, x, x + c)
            x += c
    print(x, y, count)


main()
