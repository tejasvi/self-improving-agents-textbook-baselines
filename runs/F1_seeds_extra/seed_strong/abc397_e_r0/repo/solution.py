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
    order = [1]
    parent[1] = -1
    seen = [False] * (total + 1)
    seen[1] = True
    i = 0
    while i < len(order):
        v = order[i]; i += 1
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                parent[w] = v
                order.append(w)
    cnt = [0] * (total + 1)
    ssum = [0] * (total + 1)
    h = [0] * (total + 1)
    for v in reversed(order):
        c = cnt[v]
        s = ssum[v]
        if c == 0:
            hv = 1 if k > 1 else 0
        elif c == 1:
            t = s + 1
            hv = 0 if t == k else t
        elif c == 2:
            if s + 1 == k:
                hv = 0
            else:
                print("No")
                return
        else:
            print("No")
            return
        h[v] = hv
        if v != 1 and hv > 0:
            p = parent[v]
            cnt[p] += 1
            ssum[p] += hv
    if h[1] != 0:
        print("No")
    else:
        print("Yes")

main()
