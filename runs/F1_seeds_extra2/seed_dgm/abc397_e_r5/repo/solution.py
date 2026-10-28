import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    total = n * k
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)

    if k == 1:
        print("Yes")
        return

    # Iterative DFS order from root 1
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

    # seg[v]: length of open segment (vertices, ending at v going down), or 0 if closed
    seg = [0] * (total + 1)
    # open_children[v]: list of open segment lengths from children
    open_len = [[] for _ in range(total + 1)]
    for v in reversed(order):
        lst = open_len[v]
        m = len(lst)
        if m == 0:
            s = 1
            if s == k:
                s = 0
        elif m == 1:
            s = lst[0] + 1
            if s == k:
                s = 0
        elif m == 2:
            if lst[0] + lst[1] + 1 == k:
                s = 0
            else:
                print("No")
                return
        else:
            print("No")
            return
        if v == 1:
            if s != 0:
                print("No")
                return
            break
        if s != 0:
            open_len[parent[v]].append(s)

    print("Yes")


main()
