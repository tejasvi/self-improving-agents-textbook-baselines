import sys

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
    # Root at 1, get DFS order and parents.
    parent = [0] * (m + 1)
    order = []
    visited = [False] * (m + 1)
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
    # For each vertex, r = number of vertices in the open (unfinished) path
    # that ends at v and must continue upward (r < k), or k if closed.
    open_cnt = [0] * (m + 1)
    open_a = [0] * (m + 1)
    open_b = [0] * (m + 1)
    root_r = 0
    for v in reversed(order):
        c = open_cnt[v]
        if c == 0:
            r = 1
        elif c == 1:
            r = open_a[v] + 1
        elif c == 2:
            if open_a[v] + open_b[v] + 1 != k:
                print("No")
                return
            r = k
        else:
            print("No")
            return
        if r > k:
            print("No")
            return
        if v == 1:
            root_r = r
            break
        if r < k:
            p = parent[v]
            if open_cnt[p] == 0:
                open_a[p] = r
            else:
                open_b[p] = r
            open_cnt[p] += 1
    print("Yes" if root_r == k else "No")

main()
