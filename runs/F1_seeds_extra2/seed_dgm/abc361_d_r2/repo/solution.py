import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]

    if sorted(s) != sorted(t):
        print(-1)
        return

    start = s + ".."
    target = t + ".."
    if start == target:
        print(0)
        return

    m = n + 2
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        d = dist[cur]
        k = cur.index('.')  # empty cells are k and k+1 (0-indexed)
        for x in range(m - 1):
            # stones at x and x+1 must both be present (not empty cells)
            if not (x + 1 < k or x > k + 1):
                continue
            lst = list(cur)
            a, b = lst[x], lst[x + 1]
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
