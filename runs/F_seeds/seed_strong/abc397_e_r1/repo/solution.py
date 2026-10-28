import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    m = n * k
    adj = [[] for _ in range(m + 1)]
    idx = 2
    for _ in range(m - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
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
    # val[v]: open chain length topped at v (< k), or k meaning closed
    # gather open children lengths per vertex
    open_lens = [[] for _ in range(m + 1)]
    for v in reversed(order):
        L = open_lens[v]
        cnt = len(L)
        if cnt == 0:
            res = 1
        elif cnt == 1:
            res = L[0] + 1
        elif cnt == 2:
            if L[0] + L[1] + 1 == k:
                res = k
            else:
                print("No")
                return
        else:
            print("No")
            return
        if res == k:
            res_val = k
        else:
            res_val = res
        if v == 1:
            print("Yes" if res_val == k else "No")
            return
        if res_val < k:
            open_lens[parent[v]].append(res_val)

main()
