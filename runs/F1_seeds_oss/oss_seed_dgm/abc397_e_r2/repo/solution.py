# Write your solution here. Read from stdin, write to stdout.
import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    total = N * K
    adj = [[] for _ in range(total + 1)]
    for _ in range(total - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
    # Trivial case: each vertex is a path of length 1
    if K == 1:
        print("Yes")
        return
    sys.setrecursionlimit(10 ** 6)
    def dfs(v, parent):
        pending = []  # lengths of unfinished path segments coming from children
        for to in adj[v]:
            if to == parent:
                continue
            child_len = dfs(to, v)
            if child_len == -1:
                return -1
            if child_len > 0:
                pending.append(child_len)
        # more than two unfinished segments cannot be merged at this vertex
        if len(pending) > 2:
            return -1
        if len(pending) == 2:
            a, b = pending
            if a + b + 1 != K:
                return -1
            # they together form a complete path of length K, nothing propagates upward
            return 0
        if len(pending) == 1:
            new_len = pending[0] + 1
            if new_len > K:
                return -1
            if new_len == K:
                return 0
            else:
                return new_len
        # no pending from children: start a new segment at this vertex
        return 1
    root_res = dfs(1, 0)
    if root_res == 0:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
