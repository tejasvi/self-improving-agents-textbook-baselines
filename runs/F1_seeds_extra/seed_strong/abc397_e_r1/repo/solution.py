import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    m = n * k
    if k == 1:
        print("Yes")
        return
    adj = [[] for _ in range(m + 1)]
    idx = 2
    for _ in range(m - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (m + 1)
    order = []
    visited = [False] * (m + 1)
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
    # sm[v]: number of vertices of the path-in-progress through v, counting v
    # and the open chains coming up from its children.
    # cnt[v]: number of children with an open chain (must join v).
    cnt = [0] * (m + 1)
    sm = [1] * (m + 1)
    for v in reversed(order):
        L = sm[v]
        c = cnt[v]
        if L > k or c > 2:
            print("No")
            return
        if c == 2 and L != k:
            print("No")
            return
        r = L % k
        p = parent[v]
        if p:
            if r:
                cnt[p] += 1
                sm[p] += r
        else:
            if r:
                print("No")
                return
    print("Yes")

main()
