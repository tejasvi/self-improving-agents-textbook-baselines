import sys
from collections import deque
from itertools import product


def main():
    N = int(sys.stdin.read().split()[0])

    # divisors of N
    divs = []
    i = 1
    while i * i <= N:
        if N % i == 0:
            divs.append(i)
            if i * i != N:
                divs.append(N // i)
        i += 1
    divs.sort()

    # blocks: a * rev(a) for zero-free a (at most 6 digits suffices for N <= 1e12)
    blocks = {}  # value -> token string a
    for L in range(1, 7):
        for digs in product('123456789', repeat=L):
            s = ''.join(digs)
            a = int(s)
            v = a * int(s[::-1])
            if v > 1 and v <= N and N % v == 0 and v not in blocks:
                blocks[v] = s
    block_list = list(blocks.items())

    # BFS over divisors: reachable[d] via product of blocks (unlimited use)
    parent = {1: None}
    dq = deque([1])
    while dq:
        d = dq.popleft()
        for v, s in block_list:
            nd = d * v
            if nd <= N and N % nd == 0 and nd not in parent:
                parent[nd] = (d, v)
                dq.append(nd)

    # choose optional palindromic middle M
    chosen = None
    for M in divs:
        if '0' in str(M):
            continue
        t = str(M)
        if t != t[::-1]:
            continue
        r = N // M
        if r in parent:
            chosen = (M, r)
            break

    if chosen is None:
        print(-1)
        return

    M, r = chosen
    seq = []
    cur = r
    while cur != 1:
        pd, v = parent[cur]
        seq.append(blocks[v])
        cur = pd
    left = seq
    right = [s[::-1] for s in reversed(seq)]
    tokens = left[:]
    if M != 1:
        tokens.append(str(M))
    elif not left:
        tokens.append('1')
    tokens += right
    print('*'.join(tokens))


main()
