import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    total = n * k
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
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
    # open[v]: 0 if no open child; else length of open child's path (< k)
    open_len = [0] * (total + 1)  # open child's r value, 0 if none
    r = [0] * (total + 1)
    for v in reversed(order):
        # open_len[v] holds the r of the unique open child (if any)
        if open_len[v] == 0:
            val = 1
        else:
            val = open_len[v] + 1
        if val == k:
            val = k  # closed
        r[v] = val
        p = parent[v]
        if p:
            if val < k:
                if open_len[p] != 0:
                    print("No")
                    return
                open_len[p] = val
    # root must be closed
    if r[1] == k:
        print("Yes")
    else:
        print("No")

main()
