import sys


def main():
    N = int(sys.stdin.readline())
    if N == 1:
        print("1")
        return

    # divisors of N
    n = N
    factors = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    divs = [1]
    for q, e in factors.items():
        new = []
        for d in divs:
            m = d
            for _ in range(e + 1):
                new.append(m)
                m *= q
        divs = new
    divs.sort()

    def good(x):
        return '0' not in str(x)

    # pair values v = x * rev(x) with x good, both divide N
    pair_vals = {}
    for x in divs:
        if x == 1 or not good(x):
            continue
        r = int(str(x)[::-1])
        v = x * r
        if v != 1 and N % v == 0 and v not in pair_vals:
            pair_vals[v] = x

    # reach[d] = (prev_d, v): d is a product of pair values
    reach = {1: None}
    for v, x in pair_vals.items():
        for d in divs:
            if d in reach:
                dv = d * v
                if N % dv == 0 and dv not in reach:
                    reach[dv] = (d, v)

    # choose middle palindromic good token M (or none)
    chosen = None
    for M in divs:
        if M == 1:
            mid = None
        else:
            s = str(M)
            if s != s[::-1] or not good(M):
                continue
            mid = M
        rest = N // M
        if rest in reach:
            chosen = (rest, mid)
            break

    if chosen is None:
        print(-1)
        return

    rest, mid = chosen
    xs = []
    d = rest
    while reach[d] is not None:
        pd, v = reach[d]
        xs.append(pair_vals[v])
        d = pd
    tokens = [str(x) for x in xs]
    tail = [str(x)[::-1] for x in reversed(xs)]
    seq = tokens[:]
    if mid is not None:
        seq.append(str(mid))
    seq += tail
    if not seq:
        seq = ["1"]
    print("*".join(seq))


main()
