# Write your solution here. Read from stdin, write to stdout.
import sys
sys.setrecursionlimit(1_000_000)

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
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
    # Special case: K == 1, each vertex is a path of length 1
    if K == 1:
        print("Yes")
        return
    ok = True
    def dfs(u, parent):
        nonlocal ok
        lengths = []
        for v in adj[u]:
            if v == parent:
                continue
            child_len = dfs(v, u)
            if not ok:
                return 0
            if child_len == -1:
                ok = False
                return 0
            if child_len == 0:
                continue
            cur = child_len + 1
            if cur > K:
                ok = False
                return 0
            lengths.append(cur)
        # Try to pair up lengths so that each pair sums to K.
        # Any unpaired length will be propagated upward.
        from collections import Counter
        cnt = Counter(lengths)
        for val in list(cnt.keys()):
            while cnt[val] > 0:
                need = K - val
                if need == val:
                    if cnt[val] >= 2:
                        cnt[val] -= 2
                        continue
                    else:
                        break
                else:
                    if cnt[need] > 0:
                        cnt[val] -= 1
                        cnt[need] -= 1
                        continue
                    else:
                        break
        # Collect leftovers
        leftover = []
        for val, c in cnt.items():
            leftover.extend([val] * c)
        if len(leftover) > 1:
            ok = False
            return 0
        if not leftover:
            return 0
        # One leftover length remains to be extended upward.
        val = leftover[0]
        # If it already equals K, it forms a complete path and does not need to be returned.
        if val == K:
            return 0
        return val
    root_res = dfs(1, 0)
    if not ok or root_res != 0:
        print("No")
    else:
        print("Yes")

if __name__ == "__main__":
    solve()
