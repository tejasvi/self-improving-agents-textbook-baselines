# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    outdeg = [0]*26
    indeg = [0]*26
    # adjacency for undirected component detection
    undirected_adj = [[] for _ in range(26)]
    present = [False]*26
    for _ in range(N):
        s = next(it).strip()
        a = ord(s[0]) - ord('A')
        b = ord(s[1]) - ord('A')
        outdeg[a] += 1
        indeg[b] += 1
        present[a] = present[b] = True
        undirected_adj[a].append(b)
        undirected_adj[b].append(a)
    visited = [False]*26
    ans = 0
    for v in range(26):
        if present[v] and not visited[v]:
            # BFS this weak component
            stack = [v]
            visited[v] = True
            comp_vertices = []
            while stack:
                cur = stack.pop()
                comp_vertices.append(cur)
                for nb in undirected_adj[cur]:
                    if not visited[nb]:
                        visited[nb] = True
                        stack.append(nb)
            # count sources where outdeg > indeg
            sources = 0
            for node in comp_vertices:
                if outdeg[node] > indeg[node]:
                    sources += 1
            if sources == 0:
                ans += 1
            else:
                ans += sources
    print(ans)

if __name__ == "__main__":
    solve()
