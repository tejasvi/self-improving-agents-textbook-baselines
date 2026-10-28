import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    code = {'W': 1, 'B': 2}
    start = tuple([code[c] for c in S] + [0, 0])
    target = tuple([code[c] for c in T] + [0, 0])
    if start == target:
        print(0)
        return
    # Quick check: color multisets must match
    if S.count('W') != T.count('W'):
        print(-1)
        return
    dist = {start: 0}
    q = deque([start])
    m = n + 2
    while q:
        s = q.popleft()
        d = dist[s]
        # locate empty pair
        k = s.index(0)
        for x in range(m - 1):
            if s[x] == 0 or s[x + 1] == 0:
                continue
            t = list(s)
            t[k] = s[x]
            t[k + 1] = s[x + 1]
            t[x] = 0
            t[x + 1] = 0
            tt = tuple(t)
            if tt in dist:
                continue
            if tt == target:
                print(d + 1)
                return
            dist[tt] = d + 1
            q.append(tt)
    print(-1)


main()
