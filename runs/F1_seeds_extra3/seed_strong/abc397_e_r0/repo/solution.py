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
    # L[v]: length (vertices) of open chain with top v; K means complete
    L = [0] * (M + 1)
    # for each vertex, sum of open children lengths and count, track up to 2 open
    cnt = [0] * (M + 1)      # number of open children
    s1 = [0] * (M + 1)       # sum of open children lengths
    s2 = [0] * (M + 1)       # sum of squares not needed; store first open child len
    for v in reversed(order):
        c = cnt[v]
        if c == 0:
            lv = 1
        elif c == 1:
            lv = s1[v] + 1
        elif c == 2:
            if s1[v] + 1 != K:
                print("No")
                return
            lv = K
        else:
            print("No")
            return
        L[v] = lv
        if v != 1 and lv < K:
            p = parent[v]
            cnt[p] += 1
            s1[p] += lv
    print("Yes" if L[1] == K else "No")

main()
