import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    K = int(data[1])
    V = N * K
    adj = [[] for _ in range(V + 1)]
    idx = 2
    for _ in range(V - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    # BFS order from root 1
    parent = [0] * (V + 1)
    visited = [False] * (V + 1)
    order = []
    dq = deque([1])
    visited[1] = True
    while dq:
        x = dq.popleft()
        order.append(x)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                dq.append(y)

    # f[v]: length (in vertices) of the open path hanging from v downward
    # that must be extended through parent; K means nothing is open.
    f = [0] * (V + 1)
    # pending[v]: list of open child chain lengths
    pending_cnt = [0] * (V + 1)
    pending_sum = [0] * (V + 1)
    pending_first = [0] * (V + 1)  # first open child length (for m==1)
    pending_second = [0] * (V + 1)  # second open child length (for m==2)

    for v in reversed(order):
        m = pending_cnt[v]
        if m == 0:
            res = 1
        elif m == 1:
            L1 = pending_first[v]
            res = L1 + 1
        elif m == 2:
            L1 = pending_first[v]
            L2 = pending_second[v]
            if L1 + L2 + 1 != K:
                print("No")
                return
            res = K
        else:
            print("No")
            return
        if res == K:
            res = K
        f[v] = res
        if v == 1:
            break
        if res == K:
            continue
        # open chain must be extended through parent
        p = parent[v]
        if pending_cnt[p] == 0:
            pending_first[p] = res
        else:
            pending_second[p] = res
        pending_cnt[p] += 1

    # Note: m==1 with res==K handled by the check below
    print("Yes" if f[1] == K else "No")


main()
