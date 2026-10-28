import sys


def main():
    N = int(sys.stdin.readline())

    def zero_free(s):
        return '0' not in s

    # divisors of N
    divs = []
    i = 1
    small = []
    large = []
    while i * i <= N:
        if N % i == 0:
            small.append(i)
            if i * i != N:
                large.append(N // i)
        i += 1
    divs = small + large[::-1]

    # pair factors p = x*rev(x) dividing N, p > 1, with a witness x
    pair_of = {}
    x = 1
    while True:
        s = str(x)
        if '0' not in s:
            r = int(s[::-1])
            p = x * r
            if p > N:
                # x*rev(x) >= x*1 grows; once x > N's bound stop
                if x * 10 ** (len(s) - 1) > N or x > 10 ** 6:
                    break
            elif p > 1 and N % p == 0 and p not in pair_of:
                pair_of[p] = x
        x += 1
        if x > 10 ** 6:
            break
    P = list(pair_of.keys())

    # closure: reachable divisors from 1 via multiplying pair factors
    parent = {1: None}
    stack = [1]
    while stack:
        d = stack.pop()
        for p in P:
            nd = d * p
            if N % nd == 0 and nd not in parent:
                parent[nd] = (d, p)
                stack.append(nd)

    # try palindromic zero-free divisors m as middle term
    for m in divs:
        ms = str(m)
        if ms != ms[::-1] or '0' in ms:
            continue
        t = N // m
        if t in parent:
            # reconstruct pair factors
            factors = []
            cur = t
            while parent[cur] is not None:
                d, p = parent[cur]
                factors.append(pair_of[p])
                cur = d
            left = [str(v) for v in factors]
            right = [str(v)[::-1] for v in reversed(factors)]
            terms = left + [ms] + right
            print('*'.join(terms))
            return
    print(-1)


main()
