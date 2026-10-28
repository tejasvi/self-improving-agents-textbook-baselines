import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    # bit j of seq = 1 if stone j (in order) is black
    def enc(st):
        v = 0
        for j, c in enumerate(st):
            if c == 'B':
                v |= 1 << j
        return v

    start = (n, enc(s))
    target = (n, enc(t))
    if start == target:
        print(0)
        return
    # dist array indexed by k*(2^n) + seq
    size = 1 << n
    dist = [-1] * ((n + 1) * size)
    sk, ss = start
    dist[sk * size + ss] = 0
    dq = deque([start])
    tk, ts = target
    while dq:
        k, seq = dq.popleft()
        d = dist[k * size + seq] + 1
        # stones i, i+1 physically adjacent unless i == k-1
        for i in range(n - 1):
            if i == k - 1:
                continue
            pair = (seq >> i) & 3
            low = seq & ((1 << i) - 1)
            high = seq >> (i + 2)
            rem = low | (high << i)
            if i + 1 < k:
                p = k - 2
                nk = i
            else:
                p = k
                nk = i + 2
            lo2 = rem & ((1 << p) - 1)
            hi2 = rem >> p
            nseq = lo2 | (pair << p) | (hi2 << (p + 2))
            idx = nk * size + nseq
            if dist[idx] < 0:
                dist[idx] = d
                if nk == tk and nseq == ts:
                    print(d)
                    return
                dq.append((nk, nseq))
    print(-1)


main()
