import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) - 1 for x in data[1:1 + n]]
    indeg = [0] * n
    for x in a:
        indeg[x] += 1
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
    for i in range(n):
        if on_cycle[i] and reach[i] == 0:
            # traverse cycle
            length = 0
            j = i
            while True:
                length += 1
                on_cycle[j] = True
                j = a[j]
                if j == i:
                    break
            j = i
            while True:
                reach[j] = length
                j = a[j]
                if j == i:
                    break
    for u in reversed(order):
        reach[u] = 1 + reach[a[u]]
    print(sum(reach))

main()
