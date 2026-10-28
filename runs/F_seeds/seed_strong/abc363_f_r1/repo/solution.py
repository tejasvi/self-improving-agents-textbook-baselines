import sys


def factorize(n):
    fac = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = fac.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        fac[n] = fac.get(n, 0) + 1
    return fac


def main():
    N = int(sys.stdin.read().strip())
    fac = factorize(N)
    divs = [1]
    for p, e in fac.items():
        nd = []
        for d in divs:
            x = d
            for _ in range(e + 1):
                nd.append(x)
                x *= p
        divs = nd
    divs.sort()
    divset = set(divs)

    # pair units: u = t * rev(t), t a divisor of N with no zero digit
    pair_of = {}  # unit value -> t
    for t in divs:
        s = str(t)
        if '0' in s:
            continue
        u = t * int(s[::-1])
        if N % u == 0 and u not in pair_of:
            pair_of[u] = t
    units = list(pair_of.keys())

    # good[d]: d is a product of pair units; via[d] = unit used
    good = {1: True}
    via = {}
    for d in divs:
        if d == 1:
            continue
        for u in units:
            if u <= d and d % u == 0 and good.get(d // u, False):
                good[d] = True
                via[d] = u
                break

    # choose middle palindromic token m (divisor of N, possibly 1)
    chosen_m = None
    for m in divs:
        s = str(m)
        if '0' in s or s != s[::-1]:
            continue
        if good.get(N // m, False):
            chosen_m = m
            break

    if chosen_m is None:
        print(-1)
        return

    left = []
    cur = N // chosen_m
    while cur != 1:
        u = via[cur]
        left.append(str(pair_of[u]))
        cur //= u
    tokens = left + [str(chosen_m)] + [s[::-1] for s in reversed(left)]
    print('*'.join(tokens))


main()
