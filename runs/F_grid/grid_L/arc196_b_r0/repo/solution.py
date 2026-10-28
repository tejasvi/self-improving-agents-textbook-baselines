import sys

MOD = 998244353


def solve(H, W, rows):
    # Each row and each column must contain an even number of A's.
    colpar = [0] * W
    for r in rows:
        if r.count('A') & 1:
            return 0
        for j, ch in enumerate(r):
            if ch == 'A':
                colpar[j] ^= 1
    if any(colpar):
        return 0

    # Variables: r_i for rows (nodes 0..H-1), s_j for columns (nodes H..H+W-1).
    # For B cell (i,j): r_i ^ s_j = 1 ^ P_ij ^ Q_ij, where
    #   P_ij = parity of A's in row i, columns 0..j
    #   Q_ij = parity of A's in column j, rows 0..i
    N = H + W
    parent = list(range(N))
    par = [0] * N  # parity of node relative to its parent

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        acc = 0
        for node in reversed(path):
            acc ^= par[node]
            par[node] = acc
            parent[node] = root
        return root

    def parity_to_root(x):
        root = find(x)
        return root, (par[x] if x != root else 0)

    Q = [0] * W  # running column prefix parity
    components = N
    for i in range(H):
        row = rows[i]
        P = 0
        for j in range(W):
            if row[j] == 'A':
                P ^= 1
                Q[j] ^= 1
            else:
                e = 1 ^ P ^ Q[j]
                ra, pa = parity_to_root(i)
                rb, pb = parity_to_root(H + j)
                if ra == rb:
                    if (pa ^ pb) != e:
                        return 0
                else:
                    parent[ra] = rb
                    par[ra] = pa ^ pb ^ e
                    components -= 1
    return pow(2, components, MOD)


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos])
    pos += 1
    out = []
    for _ in range(t):
        H = int(data[pos])
        W = int(data[pos + 1])
        pos += 2
        rows = [data[pos + i].decode() for i in range(H)]
        pos += H
        out.append(str(solve(H, W, rows)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
