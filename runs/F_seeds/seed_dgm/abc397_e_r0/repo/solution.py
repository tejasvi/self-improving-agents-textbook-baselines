import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    total = n * k
    if k == 1:
        print("Yes")
        return
    adj = [[] for _ in range(total + 1)]
    idx = 2
    for _ in range(total - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    parent = [0] * (total + 1)
    visited = [False] * (total + 1)
    order = []
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

    open_cnt = [0] * (total + 1)
    open_sum = [0] * (total + 1)
    for v in reversed(order):
        c = open_cnt[v]
        if c >= 3:
            print("No")
            return
        s = open_sum[v] + 1
        if c == 2:
            if s != k:
                print("No")
                return
            continue
        if s == k:
            continue
        p = parent[v]
        if p == 0:
            print("No")
            return
        open_cnt[p] += 1
        open_sum[p] += s
    print("Yes")


main()
