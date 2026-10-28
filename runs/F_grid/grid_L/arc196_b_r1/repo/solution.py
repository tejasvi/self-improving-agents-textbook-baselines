import sys

MOD = 998244353


def solve_case(H, W, S):
    # Each row must have an even number of A tiles, and each column too.
    # Horizontal edge values in row i are r_i XOR (prefix parity of A's),
    # vertical edge values in column j are c_j XOR (prefix parity of A's).
    # A B tile at (i,j) forces r_i XOR c_j = 1 XOR pl XOR ql.
    # Solutions = 2^(#components) if the parity system is consistent, else 0.
    n = H + W
    parent = list(range(n))
    par = [0] * n  # parity to parent

    def find(x):
        # returns (root, parity of x relative to root), with path compression
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        # compress: recompute parities from the top down
        acc = 0
        for node in reversed(path):
            acc ^= par[node]
            par[node] = acc
            parent[node] = root
        return root

    comps = n
    colpar = [0] * W
    for i in range(H):
        row = S[i]
        rp = 0
        for j in range(W):
            if row[j] == 'B':
                d = 1 ^ rp ^ colpar[j]
                a = i
                b = H + j
                ra = find(a)
                rb = find(b)
                pa = par[a] if a != ra else 0
                pb = par[b] if b != rb else 0
                if ra == rb:
                    if (pa ^ pb) != d:
                        return 0
                else:
                    parent[ra] = rb
                    par[ra] = pa ^ pb ^ d
                    comps -= 1
            else:
                rp ^= 1
                colpar[j] ^= 1
        if rp:
            return 0
    if any(colpar):
        return 0
    return pow(2, comps, MOD)


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        H = int(data[pos]); W = int(data[pos + 1]); pos += 2
        S = data[pos:pos + H]; pos += H
        out.append(solve_case(H, W, S))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


if __name__ == "__main__":
    main()
