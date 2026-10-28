import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]
    indeg = [0] * n
    for u in range(n):
        indeg[a[u]] += 1
    dq = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    removed = [False] * n
    while dq:
        u = dq.popleft()
        removed[u] = True
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            dq.append(v)
    reach = [0] * n
    for s in range(n):
        if not removed[s] and reach[s] == 0:
            cyc = [s]
            v = a[s]
            while v != s:
                cyc.append(v)
                v = a[v]
            L = len(cyc)
            for c in cyc:
                reach[c] = L
    for u in reversed(order):
        reach[u] = 1 + reach[a[u]]
    print(sum(reach))

main()
