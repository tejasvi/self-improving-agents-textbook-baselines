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
    parent = [0] * (M + 1)
    visited = [False] * (M + 1)
    visited[1] = True
    order = [1]
    for x in order:  # BFS (list grows while iterating)
        for y in adj[x]:
            if not visited[y]:
                visited[y] = True
                parent[y] = x
                order.append(y)
    # open_vals[v]: lengths (in vertices, 1..K-1) of unfinished paths coming up from children
    open_vals = [[] for _ in range(M + 1)]
    for v in reversed(order):
        L = open_vals[v]
        c = len(L)
        if c == 0:
            val = 1  # v starts a new path going up
        elif c == 1:
            val = L[0] + 1  # extend child's path through v
        elif c == 2:
            if L[0] + L[1] + 1 == K:  # join both children's paths through v
                val = 0
            else:
                print("No")
                return
        else:
            print("No")
            return
        if val == K:
            val = 0  # path complete at v
        if val != 0:
            if v == 1:
                print("No")  # unfinished path at root
                return
            open_vals[parent[v]].append(val)
    print("Yes")

main()
