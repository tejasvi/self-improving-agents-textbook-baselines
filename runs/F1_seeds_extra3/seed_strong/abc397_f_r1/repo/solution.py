import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    # L[i] = distinct count of a[0..i]
    L = [0] * n
    seen = set()
    for i in range(n):
        seen.add(a[i])
        L[i] = len(seen)
    # R[j] = distinct count of a[j+1..n-1]
    R = [0] * n
    seen = set()
    for j in range(n - 1, -1, -1):
        R[j] = len(seen)
        seen.add(a[j])
    # prev occurrence index (or -1)
    prev = [-1] * n
    pos = {}
    for j in range(n):
        v = a[j]
        prev[j] = pos.get(v, -1)
        pos[v] = j

    # Monotone stack of alive split indices with strictly decreasing values
    # v[i] = L[i] + distinct(a[i+1..j]).  pred[x] = previous alive index,
    # diff[x] = v[pred[x]] - v[x] > 0.  DSU nxt[] finds first alive index >= q.
    nxt = list(range(n + 1))
    pred = [-1] * n
    diff = [0] * n
    top = -1
    bottom = -1
    maxv = 0      # v[bottom]
    topv = 0      # v[top]

    def find(x):
        r = x
        while nxt[r] != r:
            r = nxt[r]
        while nxt[x] != r:
            nxt[x], x = r, nxt[x]
        return r

    best = -1
    for j in range(1, n - 1):
        x = j - 1
        lv = L[x]
        # pop dominated tops (value <= lv)
        while top != -1 and topv <= lv:
            t = top
            p = pred[t]
            nxt[t] = t + 1
            if p == -1:
                top = -1
                bottom = -1
                break
            topv += diff[t]
            top = p
        # push x
        if top == -1:
            bottom = x
            maxv = lv
            pred[x] = -1
        else:
            diff[x] = topv - lv
            pred[x] = top
        top = x
        topv = lv
        # suffix add +1 on indices >= q
        q = prev[j] if prev[j] > 0 else 0
        k = find(q)
        topv += 1
        if k == bottom:
            maxv += 1
        else:
            diff[k] -= 1
            if diff[k] == 0:
                y = pred[k]
                nxt[y] = y + 1
                if y == bottom:
                    bottom = k
                    pred[k] = -1
                else:
                    pred[k] = pred[y]
                    diff[k] = diff[y]
        cand = maxv + R[j]
        if cand > best:
            best = cand
    print(best)

main()
