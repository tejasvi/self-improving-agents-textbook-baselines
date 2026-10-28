import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    if s.count('B') != t.count('B'):
        print(-1)
        return
    if s == t:
        print(0)
        return
    m = n + 2
    start = s + '..'
    target = t + '..'
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        d = dist[cur]
        k = cur.index('.')  # empty cells are k and k+1
        for x in range(m - 1):
            # both cells x, x+1 must hold stones (not empty)
            if cur[x] == '.' or cur[x + 1] == '.':
                continue
            lst = list(cur)
            a, b = lst[x], lst[x + 1]
            lst[x] = '.'
            lst[x + 1] = '.'
            lst[k] = a
            lst[k + 1] = b
            nxt = ''.join(lst)
            if nxt not in dist:
                if nxt == target:
                    print(d + 1)
                    return
                dist[nxt] = d + 1
                q.append(nxt)
    print(-1)


main()
