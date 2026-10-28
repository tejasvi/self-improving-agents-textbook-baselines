import sys


def divisors(n):
    small, large = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i != n // i:
                large.append(n // i)
        i += 1
    return small + large[::-1]


def main():
    N = int(sys.stdin.readline().strip())
    divs = divisors(N)
    # Tokens: divisors without digit 0. Valid pair tokens v with w = v*rev(v) | N.
    pairs = {}  # w -> token v (w > 1)
    palins = []  # palindromic middle tokens (divisors)
    for v in divs:
        s = str(v)
        if '0' in s:
            continue
        r = int(s[::-1])
        if s == s[::-1]:
            palins.append(v)
        w = v * r
        if w > 1 and N % w == 0 and w not in pairs:
            pairs[w] = v
    # DP over reachable products of pair-values (parent pointers).
    parent = {1: None}
    order = [1]
    pair_list = list(pairs.items())
    for d in order:
        for w, v in pair_list:
            nd = d * w
            if nd <= N and N % nd == 0 and nd not in parent:
                parent[nd] = (d, v)
                order.append(nd)
    # Choose middle token m with N // m reachable.
    for m in palins:
        rest = N // m
        if rest in parent:
            halves = []
            cur = rest
            while parent[cur] is not None:
                d, v = parent[cur]
                halves.append(v)
                cur = d
            left = [str(v) for v in halves]
            right = [str(v)[::-1] for v in reversed(halves)]
            mid = [str(m)]
            print('*'.join(left + mid + right))
            return
    print(-1)


main()
