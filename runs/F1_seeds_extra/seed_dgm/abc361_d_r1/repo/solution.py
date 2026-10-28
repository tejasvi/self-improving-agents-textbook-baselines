import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    start = s + ".."
    target = t + ".."
    if start == target:
        print(0)
        return
    if s.count("B") != t.count("B"):
        print(-1)
        return
    dist = {start: 0}
    q = deque([start])
    m = n + 2
    while q:
        cur = q.popleft()
        d = dist[cur]
        e = cur.index(".")  # empties are at e and e+1
        for x in range(m - 1):
            if cur[x] == "." or cur[x + 1] == ".":
                continue
            lst = list(cur)
            a, b = cur[x], cur[x + 1]
            lst[x] = "."
            lst[x + 1] = "."
            lst[e] = a
            lst[e + 1] = b
            nxt = "".join(lst)
            if nxt not in dist:
                dist[nxt] = d + 1
                if nxt == target:
                    print(d + 1)
                    return
                q.append(nxt)
    print(-1)


main()
