import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    start = s + '..'
    goal = t + '..'
    if start == goal:
        print(0)
        return
    L = n + 2
    dist = {start: 0}
    dq = deque([start])
    while dq:
        cur = dq.popleft()
        d = dist[cur]
        k = cur.index('.')
        # move pair (x, x+1) of stones into empty cells (k, k+1)
        for x in range(L - 1):
            if x + 1 == k or x == k + 1 or x in (k, k + 1) or x + 1 in (k, k + 1):
                continue
            # the pair must not touch the empty cells; they are both stones
            pair = cur[x:x + 2]
            # remaining string after removing the pair and placing empties there
            rest = list(cur)
            rest[x] = '.'
            rest[x + 1] = '.'
            rest[k] = pair[0]
            rest[k + 1] = pair[1]
            nt = ''.join(rest)
            if nt not in dist:
                dist[nt] = d + 1
                if nt == goal:
                    print(d + 1)
                    return
                dq.append(nt)
    print(-1)


main()
