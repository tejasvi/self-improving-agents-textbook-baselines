import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    # Sparse table of range maxima: sp[j][i] = max(a[i : i + 2^j]).
    sp = [a]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        sp.append(list(map(max, prev[:-half], prev[half:])))
        k += 1
    LOG = len(sp)
    levels = [(1 << j, sp[j]) for j in range(LOG - 1, -1, -1)]

    pre = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += a[i]
        pre[i + 1] = s

    # memo[(l, r)] = closure sum reachable from interval [l, r] (already stable).
    memo = {}
    out = [0] * n
    for p in range(n):
        l = r = p
        S = a[p]
        path = []
        while True:
            key = l * n + r
            cached = memo.get(key)
            if cached is not None:
                S = cached
                break
            path.append(key)
            pos = l
            for step, tab in levels:
                if pos - step >= 0 and tab[pos - step] < S:
                    pos -= step
            nl = pos
            pos = r
            for step, tab in levels:
                if pos + step < n and tab[pos + 1] < S:
                    pos += step
            nr = pos
            if nl == l and nr == r:
                break
            l, r = nl, nr
            S = pre[r + 1] - pre[l]
        for key in path:
            memo[key] = S
        out[p] = S

    sys.stdout.write(" ".join(map(str, out)) + "\n")


main()
