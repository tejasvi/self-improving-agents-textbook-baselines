import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    parent = list(range(n + 2))
    lo = list(range(n + 2))
    hi = list(range(n + 2))
    col = list(range(n + 2))
    cnt = [0] * (n + 2)
    for i in range(1, n + 1):
        cnt[i] = 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    pos = 2
    for _ in range(q):
        t = data[pos]
        if t == b'1':
            x = int(data[pos + 1])
            c = int(data[pos + 2])
            pos += 3
            r = find(x)
            old = col[r]
            if old == c:
                continue
            length = hi[r] - lo[r] + 1
            cnt[old] -= length
            cnt[c] += length
            col[r] = c
            l = lo[r]
            h = hi[r]
            # merge with left neighbor
            if l > 1:
                lr = find(l - 1)
                if col[lr] == c:
                    # union lr and r
                    parent[r] = lr
                    hi[lr] = h
                    r = lr
            # merge with right neighbor
            if h < n:
                rr = find(h + 1)
                if col[rr] == c:
                    parent[rr] = r
                    hi[r] = hi[rr]
        else:
            c = int(data[pos + 1])
            pos += 2
            out.append(cnt[c])
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
