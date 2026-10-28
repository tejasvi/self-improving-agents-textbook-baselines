import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    m = n * k
    adj = [[] for _ in range(m + 1)]
    idx = 2
    for _ in range(m - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)

    # BFS order from root 1
    parent = [0] * (m + 1)
    order = []
    visited = [False] * (m + 1)
    visited[1] = True
    dq = deque([1])
    while dq:
        x = dq.popleft()
        order.append(x)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                dq.append(y)

    # open[v] = length of open path ending at v going up (0 = none/closed)
    cnt = [0] * (m + 1)   # number of open children
    sm = [0] * (m + 1)    # sum of open children lengths
    open_len = [0] * (m + 1)
    for v in reversed(order):
        c = cnt[v]
        if c > 2:
            print("No")
            return
        s = 1 + sm[v]
        if s == k:
            val = 0  # closed
        elif s < k:
            val = s
        else:
            print("No")
            return
        if v == 1:
            if val != 0:
                print("No")
                return
            break
        if val:
            p = parent[v]
            cnt[p] += 1
            sm[p] += val
    print("Yes")


main()
