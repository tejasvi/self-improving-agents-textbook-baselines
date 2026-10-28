import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    M = n * k
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
    # open_kids[v]: lengths of open (unfinished) paths hanging below v
    open_kids = [[] for _ in range(M + 1)]
    for v in reversed(order):
        L = open_kids[v]
        if len(L) == 0:
            s = 1
            res = 0 if s == k else s
        elif len(L) == 1:
            s = L[0] + 1
            res = 0 if s == k else s
        elif len(L) == 2:
            s = L[0] + L[1] + 1
            if s != k:
                print("No")
                return
            res = 0
        else:
            print("No")
            return
        if v == 1:
            if res != 0:
                print("No")
                return
        else:
            if res != 0:
                open_kids[parent[v]].append(res)
    print("Yes")

main()
