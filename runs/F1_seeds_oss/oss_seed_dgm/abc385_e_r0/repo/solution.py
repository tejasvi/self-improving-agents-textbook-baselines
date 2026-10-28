# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N)]
    for _ in range(N - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
    max_keep = 0
    # For each possible central node
    for r in range(N):
        caps = []
        for v in adj[r]:
            cap = len(adj[v]) - 1  # neighbors excluding r
            caps.append(cap)
        if not caps:
            continue
        caps.sort(reverse=True)
        # iterate over i (1-indexed)
        for i, y in enumerate(caps, start=1):
            if y < 1:
                break  # further values are <= y
            keep = 1 + i * (y + 1)
            if keep > max_keep:
                max_keep = keep
    # It's always possible to have at least 3 vertices (x=1, y=1)
    if max_keep < 3:
        max_keep = 3
    answer = N - max_keep
    print(answer)

if __name__ == "__main__":
    solve()
