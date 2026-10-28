import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    total = n * k
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    # BFS order from root 1
    parent = [0] * (total + 1)
    order = []
    visited = [False] * (total + 1)
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

    # open[v] = length of unfinished chain starting at v going down (0 = none)
    open_len = [0] * (total + 1)
    # cnt[v] = number of children with open chain, best[v] = their open length (sum-like)
    cnt = [0] * (total + 1)
    child_sum = [0] * (total + 1)

    for v in reversed(order):
        c = cnt[v]
        if c >= 3:
            print("No")
            return
        if c == 0:
            g = 1 if k > 1 else 0
        elif c == 1:
            g = child_sum[v] + 1
            if g >= k:
                g = 0
        else:
            # two open chains meet at v and must close a path of exactly K vertices
            if child_sum[v] + 1 != k:
                print("No")
                return
            g = 0
        open_len[v] = g
        p = parent[v]
        if p and g > 0:
            cnt[p] += 1
            child_sum[p] += g

    if open_len[1] != 0:
        print("No")
    else:
        print("Yes")


main()
