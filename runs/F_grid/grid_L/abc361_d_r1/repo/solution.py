import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]

    def enc(st):
        c = 0
        for i, ch in enumerate(st):
            if ch == 'B':
                c |= 1 << i
        return c

    start = (enc(s), n)  # bit i = 1 if cell i (0-indexed) holds black stone; empties at k, k+1
    target = (enc(t), n)
    if start == target:
        print(0)
        return

    dist = {start: 0}
    dq = deque([start])
    while dq:
        state = dq.popleft()
        c, k = state
        d = dist[state] + 1
        # choose pair x, x+1 both stones: x+1 < k or x > k+1
        for x in range(0, n + 1):
            if x + 1 >= k and x <= k + 1:
                continue
            if x + 1 >= n + 2:
                break
            a = (c >> x) & 1
            b = (c >> (x + 1)) & 1
            c2 = c & ~(3 << x)
            c2 &= ~(3 << k)
            c2 |= (a << k) | (b << (k + 1))
            ns = (c2, x)
            if ns not in dist:
                if ns == target:
                    print(d)
                    return
                dist[ns] = d
                dq.append(ns)
    print(-1)


main()
