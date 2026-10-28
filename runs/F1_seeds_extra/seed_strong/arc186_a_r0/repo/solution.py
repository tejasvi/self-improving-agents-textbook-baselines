import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); q = int(data[1])
    ks = [int(x) for x in data[2:2 + q]]
    # reach[a][b]: bitset of achievable free-cell counts using exactly a rows, b cols
    # in disjoint blocks of size r x c (r, c >= 2).  Free = sum r*c.
    reach = [[0] * (n + 1) for _ in range(n + 1)]
    reach[0][0] = 1
    items = [(r, c) for r in range(2, n + 1) for c in range(2, n + 1)]
    for a in range(n + 1):
        for b in range(n + 1):
            cur = reach[a][b]
            for (r, c) in items:
                if r <= a and c <= b:
                    prev = reach[a - r][b - c]
                    if prev:
                        cur |= prev << (r * c)
            reach[a][b] = cur
    free_ok = 0
    for a in range(n + 1):
        for b in range(n + 1):
            free_ok |= reach[a][b]
    out = []
    total = n * n
    for k in ks:
        f = total - k
        if 0 <= f <= total and (free_ok >> f) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")

main()
