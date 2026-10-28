# Write your solution here. Read from stdin, write to stdout.

import sys

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))

    parent = list(range(N + 1))
    size = [1] * (N + 1)
    left = list(range(N + 1))
    right = list(range(N + 1))
    color = list(range(N + 1))  # color[i] is valid for root i
    cnt = [0] * (N + 1)
    for i in range(1, N + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return a
        # both components have the same color already
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        left[a] = min(left[a], left[b])
        right[a] = max(right[a], right[b])
        # color remains the same (both are same)
        return a

    out_lines = []
    for _ in range(Q):
        t = int(next(it))
        if t == 1:
            x = int(next(it))
            c = int(next(it))
            root = find(x)
            cur_color = color[root]
            if cur_color != c:
                # update global counts
                cnt[cur_color] -= size[root]
                cnt[c] += size[root]
                color[root] = c
            # try merging with left neighbors
            while True:
                root = find(root)
                l = left[root]
                if l == 1:
                    break
                nb = l - 1
                nroot = find(nb)
                if color[nroot] == c and nroot != root:
                    root = union(root, nroot)
                else:
                    break
            # try merging with right neighbors
            while True:
                root = find(root)
                r = right[root]
                if r == N:
                    break
                nb = r + 1
                nroot = find(nb)
                if color[nroot] == c and nroot != root:
                    root = union(root, nroot)
                else:
                    break
        else:
            c = int(next(it))
            out_lines.append(str(cnt[c]))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
