import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    total = n * k
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    # iterative DFS order from root 1
    parent = [0] * (total + 1)
    order = []
    visited = [False] * (total + 1)
    stack = [1]
    visited[1] = True
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if not visited[w]:
                visited[w] = True
                parent[w] = v
                stack.append(w)
    # ret[v]: 0 if closed, else number of vertices of open path ending at v (going up)
    open_a = [0] * (total + 1)  # first open child length
    open_b = [0] * (total + 1)
    open_cnt = [0] * (total + 1)
    ret = [0] * (total + 1)
    for v in reversed(order):
        c = open_cnt[v]
        if c == 0:
            r = 1 if k > 1 else 0
        elif c == 1:
            cur = open_a[v] + 1
            r = 0 if cur == k else cur
        elif c == 2:
            if open_a[v] + open_b[v] + 1 == k:
                r = 0
            else:
                print("No")
                return
        else:
            print("No")
            return
        ret[v] = r
        p = parent[v]
        if p and r:
            if open_cnt[p] == 0:
                open_a[p] = r
            else:
                open_b[p] = r
            open_cnt[p] += 1
            if open_cnt[p] > 2:
                print("No")
                return
    if ret[1] != 0:
        print("No")
    else:
        print("Yes")

main()
