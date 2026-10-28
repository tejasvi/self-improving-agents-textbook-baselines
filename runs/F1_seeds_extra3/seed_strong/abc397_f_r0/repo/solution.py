import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [0] + [int(x) for x in data[1:1 + n]]  # 1-indexed

    L = [0] * (n + 2)
    seen = bytearray(n + 2)
    c = 0
    for i in range(1, n + 1):
        if not seen[a[i]]:
            seen[a[i]] = 1
            c += 1
        L[i] = c
    R = [0] * (n + 2)
    seen = bytearray(n + 2)
    c = 0
    for k in range(n, 0, -1):
        if not seen[a[k]]:
            seen[a[k]] = 1
            c += 1
        R[k] = c

    prev = [0] * (n + 1)
    last = [0] * (n + 2)
    for j in range(1, n + 1):
        prev[j] = last[a[j]]
        last[a[j]] = j

    # Monotonic "stack" of candidate i's (value val_i = L[i] + distinct(i+1..j)).
    # Candidates are alive indices with strictly decreasing values left to right.
    # Dead indices point (via nxt) to a larger index; find() gives first alive >= x.
    nxt = list(range(n + 2))
    prv = [0] * (n + 2)
    diff = [0] * (n + 2)  # diff[b] = val[prv[b]] - val[b]
    head = 0      # first alive index (0 = none)
    headval = 0
    tail = 0      # last alive index (0 = none)
    tailval = 0

    def find(x):
        root = x
        while nxt[root] != root:
            root = nxt[root]
        while nxt[x] != root:
            nxt[x], x = root, nxt[x]
        return root

    best = 0
    for j in range(1, n + 1):
        if j >= 2:
            idx = j - 1
            x = L[idx]
            # pop dominated tail elements (value <= x)
            while tail and tailval <= x:
                T = tail
                nxt[T] = T + 1
                P = prv[T]
                if P:
                    tailval += diff[T]
                    tail = P
                else:
                    tail = 0
                    head = 0
            if tail:
                diff[idx] = tailval - x
                prv[idx] = tail
            else:
                head = idx
                headval = x
                prv[idx] = 0
            tail = idx
            tailval = x
        if j >= 2:
            # suffix add +1 on candidates with index in [lo, j-1]
            pv = prev[j]
            lo = pv if pv >= 1 else 1
            if lo <= j - 1:
                tailval += 1
                b = find(lo)
                if b == head:
                    headval += 1
                else:
                    diff[b] -= 1
                    if diff[b] == 0:
                        ap = prv[b]  # remove ap (dominated by b now)
                        nxt[ap] = ap + 1
                        p = prv[ap]
                        prv[b] = p
                        if p:
                            diff[b] = diff[ap]
                        else:
                            head = b  # headval unchanged (equal to old head value)
            if j + 1 <= n:
                val = headval + R[j + 1]
                if val > best:
                    best = val
    print(best)

main()
