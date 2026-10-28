import sys


def factorize(n):
    fs = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs[d] = fs.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        fs[n] = fs.get(n, 0) + 1
    return fs


def divisors_of(fs):
    divs = [1]
    for p, e in fs.items():
        new = []
        for d in divs:
            x = d
            for _ in range(e + 1):
                new.append(x)
                x *= p
        divs = new
    divs.sort()
    return divs


def main():
    N = int(sys.stdin.read().split()[0])
    fs = factorize(N)
    D = divisors_of(fs)
    Dset = set(D)

    # pair blocks: f * rev(f) with f digits nonzero, f | N, f*rev(f) | N
    block_f = {}  # block value -> f string
    for f in D:
        s = str(f)
        if '0' in s:
            continue
        r = s[::-1]
        b = f * int(r)
        if b <= N and N % b == 0:
            if b not in block_f:
                block_f[b] = s
    blocks = [b for b in block_f if b > 1]

    # reachability over divisors via unbounded knapsack
    R = {1: True}
    par = {}
    for b in blocks:
        for d in D:
            if d % b == 0 and R.get(d // b, False) and d not in R:
                R[d] = True
                par[d] = b

    # middle palindrome options M (divisor of N, nonzero digits, palindrome) or none
    chosen_M = None
    if N in R:
        chosen_M = 1
    else:
        for M in D:
            s = str(M)
            if '0' in s or s != s[::-1]:
                continue
            q = N // M
            if q in R:
                chosen_M = M
                break
    if chosen_M is None:
        print(-1)
        return

    # reconstruct pair blocks
    left = []
    d = N // chosen_M
    while d > 1:
        b = par[d]
        left.append(block_f[b])
        d //= b

    parts = left + ([str(chosen_M)] if chosen_M != 1 else [])
    right = [s[::-1] for s in reversed(left)]
    if not parts and not right:
        print(1)
        return
    if chosen_M == 1 and not left:
        print(1)
        return
    res = left + ([str(chosen_M)] if chosen_M != 1 else []) + right
    print('*'.join(res))


main()
