import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); K = int(data[1])
    M = N * K
    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (M + 1)
    order = []
    visited = [False] * (M + 1)
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
    # f[v]: length of open chain starting at v going down; K means closed
    f = [0] * (M + 1)
    open_children = [[] for _ in range(M + 1)]
    ok = True
    for v in reversed(order):
        oc = open_children[v]
        if len(oc) == 0:
            fv = 1
        elif len(oc) == 1:
            fv = oc[0] + 1
        elif len(oc) == 2:
            if oc[0] + oc[1] + 1 != K:
                ok = False
                break
            fv = K
        else:
            ok = False
            break
        if fv > K:
            ok = False
            break
        f[v] = fv
        if v == 1:
            if fv != K:
                ok = False
            break
        if fv < K:
            open_children[parent[v]].append(fv)
    print("Yes" if ok else "No")

main()
