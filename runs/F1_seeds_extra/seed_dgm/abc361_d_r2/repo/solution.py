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
    dist = {start: 0}
    q = deque([start])
    L = n + 2
    while q:
        cur = q.popleft()
        d = dist[cur]
        k = cur.index(".")  # empty cells are k and k+1
        for x in range(L - 1):
            if cur[x] == "." or cur[x + 1] == ".":
                continue  # pair must both contain stones
            lst = list(cur)
            lst[k] = cur[x]
            lst[k + 1] = cur[x + 1]
            lst[x] = "."
            lst[x + 1] = "."
            nxt = "".join(lst)
            if nxt not in dist:
                dist[nxt] = d + 1
                if nxt == target:
                    print(d + 1)
                    return
                q.append(nxt)
    print(-1)


main()
