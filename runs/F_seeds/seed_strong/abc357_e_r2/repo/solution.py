import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]
    indeg = [0] * n
    for x in a:
        indeg[x] += 1
    # Peel leaves (Kahn's algorithm); remaining vertices lie on cycles.
    order = [i for i in range(n) if indeg[i] == 0]
    head = 0
    while head < len(order):
        u = order[head]
        head += 1
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            order.append(v)
    reach = [0] * n
    on_cycle = [indeg[i] > 0 for i in range(n)]
    done = [False] * n
    for s in range(n):
        if on_cycle[s] and not done[s]:
            length = 0
            v = s
            while True:
                done[v] = True
                length += 1
                v = a[v]
                if v == s:
                    break
            v = s
            for _ in range(length):
                reach[v] = length
                v = a[v]
    for u in reversed(order):
        reach[u] = reach[a[u]] + 1
    print(sum(reach))


main()
