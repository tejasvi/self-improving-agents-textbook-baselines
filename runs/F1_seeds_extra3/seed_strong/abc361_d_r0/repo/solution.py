import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1]
    T = data[2]
    start = S + '..'
    target = T + '..'
    if start == target:
        print(0)
        return
    dist = {start: 0}
    dq = deque([start])
    L = n + 2
    while dq:
        s = dq.popleft()
        d = dist[s]
        # find empty pair position
        k = s.index('.')
        nd = d + 1
        for x in range(L - 1):
            if s[x] != '.' and s[x + 1] != '.':
                # move stones at x,x+1 to k,k+1
                lst = list(s)
                a = lst[x]; b = lst[x + 1]
                lst[x] = '.'; lst[x + 1] = '.'
                lst[k] = a; lst[k + 1] = b
                t = ''.join(lst)
                if t not in dist:
                    if t == target:
                        print(nd)
                        return
                    dist[t] = nd
                    dq.append(t)
    print(-1)

main()
