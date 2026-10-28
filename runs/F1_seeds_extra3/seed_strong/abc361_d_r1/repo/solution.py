import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    # State: (k, seq) where empty cells are k, k+1 (0-indexed, 0..N),
    # seq is the color string of the N stones in left-to-right order.
    start = (n, S)
    target = (n, T)
    if start == target:
        print(0)
        return
    dist = {start: 0}
    dq = deque([start])
    while dq:
        state = dq.popleft()
        k, s = state
        d = dist[state] + 1
        # Pair entirely left of the gap: cells x, x+1 with x+1 <= k-1
        for x in range(0, k - 1):
            pair = s[x:x + 2]
            rest = s[:x] + s[x + 2:]
            p = k - 2
            ns = rest[:p] + pair + rest[p:]
            nxt = (x, ns)
            if nxt not in dist:
                dist[nxt] = d
                if nxt == target:
                    print(d)
                    return
                dq.append(nxt)
        # Pair entirely right of the gap: cells x, x+1 with x >= k+2, x+1 <= n+1
        for x in range(k + 2, n + 1):
            i = x - 2
            pair = s[i:i + 2]
            rest = s[:i] + s[i + 2:]
            ns = rest[:k] + pair + rest[k:]
            nxt = (x, ns)
            if nxt not in dist:
                dist[nxt] = d
                if nxt == target:
                    print(d)
                    return
                dq.append(nxt)
    print(-1)


main()
