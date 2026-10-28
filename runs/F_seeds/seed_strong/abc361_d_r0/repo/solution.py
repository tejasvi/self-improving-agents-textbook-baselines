import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    def enc(str_):
        v = 0
        for i, c in enumerate(str_):
            if c == 'B':
                v |= 1 << i
        return v
    s0 = enc(S)
    tgt = enc(T)
    # state: (k, s) where empty cells are k, k+1 (0-based); s = stone colours in order
    # encode as k * 2^n + s
    start = (n << n) | s0  # k = n (empty pair at the end)
    target = (n << n) | tgt
    if start == target:
        print(0)
        return
    dist = {start: 0}
    dq = deque([start])
    mask_all = (1 << n) - 1
    while dq:
        st = dq.popleft()
        d = dist[st]
        k = st >> n
        s = st & mask_all
        nd = d + 1
        # pairs fully to the left of the empty block: x in [0, k-2]
        for x in range(0, k - 1):
            v = (s >> x) & 3
            low = s & ((1 << x) - 1)
            high = s >> (x + 2)
            rest = low | (high << x)
            b = k - 2
            low2 = rest & ((1 << b) - 1)
            high2 = rest >> b
            ns = low2 | (v << b) | (high2 << (b + 2))
            nst = (x << n) | ns
            if nst not in dist:
                dist[nst] = nd
                if nst == target:
                    print(nd)
                    return
                dq.append(nst)
        # pairs to the right: x in [k+2, n-1]
        for x in range(k + 2, n + 1):
            a = x - 2
            v = (s >> a) & 3
            low = s & ((1 << a) - 1)
            high = s >> (a + 2)
            rest = low | (high << a)
            b = k
            low2 = rest & ((1 << b) - 1)
            high2 = rest >> b
            ns = low2 | (v << b) | (high2 << (b + 2))
            nst = (x << n) | ns
            if nst not in dist:
                dist[nst] = nd
                if nst == target:
                    print(nd)
                    return
                dq.append(nst)
    print(-1)

main()
