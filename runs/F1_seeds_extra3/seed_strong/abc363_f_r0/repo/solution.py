import sys


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def main():
    N = int(sys.stdin.readline())
    fac = factorize(N)
    divs = [1]
    for p, e in fac.items():
        nd = []
        for d in divs:
            v = d
            for _ in range(e + 1):
                nd.append(v)
                v *= p
        divs = nd
    divs.sort()

    # Candidate pairs (x, rev(x)) with x*rev(x) dividing N, x zero-free, x > 1.
    pairs = []
    for d in divs:
        if d == 1:
            continue
        s = str(d)
        if '0' in s:
            continue
        r = int(s[::-1])
        pv = d * r
        if N % pv == 0:
            pairs.append((pv, d, r))

    # reach[d] = (prev, x, r) : d = product of pair values, built ascending.
    reach = {1: None}
    for d in divs:
        if d not in reach:
            continue
        for pv, x, r in pairs:
            nd = d * pv
            if N % nd == 0 and nd not in reach:
                reach[nd] = (d, x, r)

    for M in divs:
        s = str(M)
        if '0' in s or s != s[::-1]:
            continue
        rest = N // M
        if rest not in reach:
            continue
        L = []
        R = []
        cur = rest
        while cur != 1:
            prev, x, r = reach[cur]
            L.append(str(x))
            R.append(str(r))
            cur = prev
        tokens = L + [s] + list(reversed(R))
        print('*'.join(tokens))
        return
    print(-1)


main()
