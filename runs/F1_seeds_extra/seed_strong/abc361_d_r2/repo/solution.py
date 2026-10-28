import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    start = S + '..'
    goal = T + '..'
    if start == goal:
        print(0)
        return
    # The multiset of colors must match, otherwise impossible.
    if S.count('B') != T.count('B'):
        print(-1)
        return
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        d = dist[s]
        # locate gap
        k = s.index('..')
        for x in range(n + 1):
            if s[x] == '.' or s[x + 1] == '.':
                continue
            t = list(s)
            a = t[x]; b = t[x + 1]
            t[x] = '.'; t[x + 1] = '.'
            t[k] = a; t[k + 1] = b
            ns = ''.join(t)
            if ns not in dist:
                nd = d + 1
                if ns == goal:
                    print(nd)
                    return
                dist[ns] = nd
                q.append(ns)
    print(-1)

main()
