import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    start = s + '..'
    target = t + '..'
    if start == target:
        print(0)
        return
    # sorted color counts must match, else impossible
    if sorted(s) != sorted(t):
        print(-1)
        return
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        d = dist[cur]
        k = cur.index('..')
        for x in range(n + 1):
            # cells x and x+1 both stones
            if x + 1 == k or x == k + 1 or x + 1 == k + 1 or x == k:
                continue
            # cells x,x+1 not in gap [k,k+1]
            pair = cur[x:x + 2]
            nxt = cur[:x] + '..' + cur[x + 2:]
            # place pair at gap positions k,k+1 in nxt (which has gap at x..x+1)
            lst = list(nxt)
            lst[k] = pair[0]
            lst[k + 1] = pair[1]
            nw = ''.join(lst)
            if nw not in dist:
                dist[nw] = d + 1
                if nw == target:
                    print(d + 1)
                    return
                q.append(nw)
    print(-1)

main()
