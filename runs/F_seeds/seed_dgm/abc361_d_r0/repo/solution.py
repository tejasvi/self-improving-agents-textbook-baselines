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
    start = s + "EE"
    goal = t + "EE"
    if start == goal:
        print(0)
        return
    dist = {start: 0}
    dq = deque([start])
    while dq:
        cur = dq.popleft()
        d = dist[cur]
        k = cur.index("E")  # gap is at cells k, k+1
        for x in range(n + 1):
            if cur[x] == "E" or cur[x + 1] == "E":
                continue
            lst = list(cur)
            lst[k] = cur[x]
            lst[k + 1] = cur[x + 1]
            lst[x] = "E"
            lst[x + 1] = "E"
            nxt = "".join(lst)
            if nxt not in dist:
                dist[nxt] = d + 1
                if nxt == goal:
                    print(d + 1)
                    return
                dq.append(nxt)
    print(-1)


main()
