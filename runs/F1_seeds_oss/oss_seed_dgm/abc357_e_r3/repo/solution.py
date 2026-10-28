# Write your solution here. Read from stdin, write to stdout.
import sys
sys.setrecursionlimit(1 << 25)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(next(it))

    state = [0] * (n + 1)  # 0=unvisited,1=visiting,2=processed
    size = [0] * (n + 1)   # reachable count for each vertex

    def dfs(u: int):
        state[u] = 1
        v = a[u]
        if state[v] == 0:
            dfs(v)
            if size[u] == 0:
                size[u] = size[v] + 1
        elif state[v] == 1:
            # found a new cycle; collect its nodes
            cycle_nodes = []
            x = v
            while True:
                cycle_nodes.append(x)
                if x == u:
                    break
                x = a[x]
            clen = len(cycle_nodes)
            for node in cycle_nodes:
                size[node] = clen
        else:  # state[v] == 2, already processed
            size[u] = size[v] + 1
        state[u] = 2

    for i in range(1, n + 1):
        if state[i] == 0:
            dfs(i)

    total = sum(size[1:])
    print(total)

if __name__ == "__main__":
    main()
