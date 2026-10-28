# Buildings 2 solution
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    H = [0] * (N + 1)
    for i in range(1, N + 1):
        H[i] = int(next(it))
    # next greater element to the right (first taller building)
    nxt = [0] * (N + 1)  # 0 means no taller building
    stack = []
    for i in range(N, 0, -1):
        while stack and H[stack[-1]] < H[i]:
            stack.pop()
        nxt[i] = stack[-1] if stack else 0
        stack.append(i)
    # depth: number of steps from i following nxt until 0
    depth = [0] * (N + 1)
    for i in range(N, 0, -1):
        if nxt[i]:
            depth[i] = depth[nxt[i]] + 1
        else:
            depth[i] = 0
    LOG = (N + 1).bit_length()
    up = [[0] * (N + 1) for _ in range(LOG)]
    up[0] = nxt[:]  # first ancestor
    for k in range(1, LOG):
        upk = up[k]
        upkm1 = up[k - 1]
        for i in range(1, N + 1):
            p = upkm1[i]
            upk[i] = upkm1[p] if p else 0
    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # lift a up to depth of b
        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return nxt[a]
    out = []
    for _ in range(Q):
        l = int(next(it))
        r = int(next(it))
        w = lca(l, r)
        if w == 0:
            out.append('0')
            continue
        if w > r:
            out.append(str(depth[w]))
            continue
        # w <= r, need first ancestor > r
        cur = w
        for k in range(LOG - 1, -1, -1):
            nxt_node = up[k][cur]
            if nxt_node and nxt_node <= r:
                cur = nxt_node
        anc = nxt[cur]
        if anc == 0:
            out.append('0')
        else:
            out.append(str(depth[anc]))
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
