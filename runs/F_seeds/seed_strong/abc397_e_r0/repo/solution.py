import sys

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
    # iterative DFS order from root 1
    parent = [0] * (M + 1)
    order = []
    visited = [False] * (M + 1)
    stack = [1]
    visited[1] = True
    while stack:
        x = stack.pop()
        order.append(x)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                stack.append(y)
    f = [0] * (M + 1)
    # collect open child lengths per vertex
    open1 = [0] * (M + 1)  # first open child length
    open2 = [0] * (M + 1)  # second open child length
    cnt = [0] * (M + 1)
    for v in reversed(order):
        c = cnt[v]
        if c == 0:
            val = 1
        elif c == 1:
            val = open1[v] + 1
        elif c == 2:
            if open1[v] + open2[v] + 1 != K:
                print("No")
                return
            val = 0
        else:
            print("No")
            return
        if val == K:
            val = 0
        f[v] = val
        p = parent[v]
        if p and val:
            if cnt[p] == 0:
                open1[p] = val
            elif cnt[p] == 1:
                open2[p] = val
            cnt[p] += 1
            if cnt[p] > 2:
                # will be caught when processing parent; keep count
                pass
    if f[1] != 0:
        print("No")
    else:
        print("Yes")

main()
