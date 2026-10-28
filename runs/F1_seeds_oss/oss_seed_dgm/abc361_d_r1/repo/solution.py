# Write your solution here. Read from stdin, write to stdout.

import sys
from collections import deque

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    S = next(it).strip()
    T = next(it).strip()
    # quick check: counts of B and W must match
    if S.count('B') != T.count('B') or S.count('W') != T.count('W'):
        print(-1)
        return
    L = N + 2
    start = S + '..'   # empty cells at the right end
    target = T + '..'
    if start == target:
        print(0)
        return
    dq = deque([start])
    dist = {start: 0}
    while dq:
        cur = dq.popleft()
        d = dist[cur]
        e = cur.find('..')  # position of empty pair (0-indexed)
        # try moving any adjacent stone pair to the empty slots
        for x in range(L - 1):
            if x == e:
                continue
            if cur[x] == '.' or cur[x+1] == '.':
                continue
            lst = list(cur)
            # move stones
            lst[e] = cur[x]
            lst[e+1] = cur[x+1]
            lst[x] = '.'
            lst[x+1] = '.'
            nxt = ''.join(lst)
            if nxt not in dist:
                if nxt == target:
                    print(d + 1)
                    return
                dist[nxt] = d + 1
                dq.append(nxt)
    print(-1)

if __name__ == "__main__":
    solve()
