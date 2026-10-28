import sys


def main():
    N = int(sys.stdin.readline().strip())

    # divisors of N
    divs = []
    i = 1
    while i * i <= N:
        if N % i == 0:
            divs.append(i)
            if i != N // i:
                divs.append(N // i)
        i += 1
    divs.sort()

    def valid_digits(s):
        return '0' not in s

    # pair products p = x * rev(x) that divide N, with a representative x
    pair_rep = {}
    for x in divs:
        if x == 1 or x > 10**6:
            continue
        xs = str(x)
        if not valid_digits(xs):
            continue
        r = int(xs[::-1])
        p = x * r
        if N % p == 0 and p > 1 and p not in pair_rep:
            pair_rep[p] = xs
    pairs = list(pair_rep.keys())

    # reachability over divisors: reach[d] = (prev_d, p) meaning d = prev_d * p
    parent = {1: None}
    queue = [1]
    qi = 0
    while qi < len(queue):
        d = queue[qi]
        qi += 1
        for p in pairs:
            nd = d * p
            if N % nd == 0 and nd not in parent:
                parent[nd] = (d, p)
                queue.append(nd)

    # find palindromic middle M (digits 1-9) with N/M reachable
    for M in divs:
        s = str(M)
        if '0' in s or s != s[::-1]:
            continue
        rest = N // M
        if rest not in parent:
            continue
        # reconstruct pair list
        plist = []
        cur = rest
        while parent[cur] is not None:
            prev, p = parent[cur]
            plist.append(pair_rep[p])
            cur = prev
        left = plist
        tokens = left + [s] + [t[::-1] for t in reversed(left)]
        print('*'.join(tokens))
        return
    print(-1)


main()
