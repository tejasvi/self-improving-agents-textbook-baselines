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
    visited = [False] * (m + 1)
    order = []
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

    # ret[v] = length of open chain starting at v going down (including v),
    # or 0 if no chain needs to continue upward.
    ret = [0] * (m + 1)
    open_children = [[] for _ in range(m + 1)]
    for v in reversed(order):
        ch = open_children[v]
        if len(ch) > 2:
            print("No")
            return
        if len(ch) == 2:
            a, b = ch
            if a + b + 1 != k:
                print("No")
                return
            r = 0
        elif len(ch) == 1:
            a = ch[0]
            r = 0 if a + 1 == k else a + 1
        else:
            r = 1 if k > 1 else 0
        ret[v] = r
        if v != 1 and r != 0:
            open_children[parent[v]].append(r)

    print("Yes" if ret[1] == 0 else "No")


main()
