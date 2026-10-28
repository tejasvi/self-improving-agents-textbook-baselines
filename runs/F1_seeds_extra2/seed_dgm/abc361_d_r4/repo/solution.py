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
    # Quick check: color counts must match
    if sorted(s) != sorted(t):
        print(-1)
        return
    dist = {start: 0}
    q = deque([start])
    L = n + 2
    while q:
        cur = q.popleft()
        d = dist[cur]
        # empty pair position k (0-indexed): first '.'
        k = cur.index('.')
        for x in range(L - 1):
            if cur[x] == '.' or cur[x + 1] == '.':
                continue
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
