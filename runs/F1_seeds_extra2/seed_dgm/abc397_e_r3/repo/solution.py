import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    total = n * k
    if total == 1:
        print("Yes")
        return
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
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
    # open[v]: list of f values of children that are unfinished (<k)
    open_cnt = [0] * (total + 1)   # number of unfinished children
    open_sum = [0] * (total + 1)   # sum of f of unfinished children
    open_a = [0] * (total + 1)     # f of first unfinished child
    open_b = [0] * (total + 1)     # f of second unfinished child
    f = [0] * (total + 1)
    for v in reversed(order):
        c = open_cnt[v]
        if c == 0:
            fv = 1
        elif c == 1:
            fv = open_a[v] + 1
        elif c == 2:
            if open_a[v] + open_b[v] + 1 != k:
                print("No")
                return
            fv = k
        else:
            print("No")
            return
        if fv > k:
            print("No")
            return
        f[v] = fv
        p = parent[v]
        if v != 1 and fv < k:
            if open_cnt[p] == 0:
                open_a[p] = fv
            else:
                open_b[p] = fv
            open_cnt[p] += 1
    if f[1] != k:
        print("No")
    else:
        print("Yes")

main()
