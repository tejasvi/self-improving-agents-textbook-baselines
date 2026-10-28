import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    if sorted(S) != sorted(T):
        print(-1)
        return
    # state: string of length n+2, '.' for empty cells
    start = S + '..'
    target = T + '..'
    if start == target:
        print(0)
        return
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        d = dist[cur]
        k = cur.index('.')  # empty cells k, k+1
        for x in range(0, n + 1):
            # cells x and x+1 must both be stones
            if k - 1 <= x <= k + 1:
                continue  # cell x or x+1 is empty
            # build new state
            lst = list(cur)
            a = lst[x]
            b = lst[x + 1]
            lst[x] = '.'
            lst[x + 1] = '.'
            lst[k] = a
            lst[k + 1] = b
            nxt = ''.join(lst)
            if nxt not in dist:
                dist[nxt] = d + 1
                if nxt == target:
                    print(d + 1)
                    return
                q.append(nxt)
    print(-1)


main()
