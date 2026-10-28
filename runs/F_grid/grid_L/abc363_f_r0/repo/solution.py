import sys
from collections import deque


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


def divisors(n):
    divs = [1]
    for p, e in factorize(n).items():
        new = []
        for d in divs:
            x = d
            for _ in range(e + 1):
                new.append(x)
                x *= p
        divs = new
    return sorted(divs)


def zeroless(s):
    return '0' not in s


def main():
    N = int(sys.stdin.read().split()[0])
    divs = divisors(N)
    divset = set(divs)

    # Units: pair (x, rev(x)) with value x*rev(x) dividing N.
    units = {}  # value -> token string x (first of the pair)
    for x in divs:
        s = str(x)
        if not zeroless(s):
            continue
        r = s[::-1]
        rv = int(r)
        if rv not in divset:
            continue
        v = x * rv
        if v == 1 or N % v != 0:
            continue
        if v not in units:
            units[v] = s

    # BFS over divisors of N: reach[d] = (prev_d, unit_value)
    parent = {1: None}
    dq = deque([1])
    unit_items = list(units.items())
    while dq:
        d = dq.popleft()
        for v, _ in unit_items:
            nd = d * v
            if N % nd == 0 and nd not in parent:
                parent[nd] = (d, v)
                dq.append(nd)

    def build_units(target):
        seq = []
        cur = target
        while cur != 1:
            pd, v = parent[cur]
            seq.append(units[v])
            cur = pd
        return seq

    # Choose middle token (palindromic zeroless divisor) or none.
    middle = None
    rest = None
    for m in sorted(divs, reverse=True):
        s = str(m)
        if s == s[::-1] and zeroless(s):
            q = N // m
            if q in parent:
                middle = s
                rest = q
                break
    if middle is None:
        if N in parent:
            rest = N
        else:
            print(-1)
            return

    seq = build_units(rest)  # list of left-half token strings
    left = [s for s in seq]
    right = [s[::-1] for s in reversed(seq)]
    tokens = left + ([middle] if middle is not None else []) + right
    if not tokens:
        tokens = ['1']
    print('*'.join(tokens))


main()
