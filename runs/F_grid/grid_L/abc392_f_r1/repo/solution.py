import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    p = [0] * (n + 1)
    for i in range(1, n + 1):
        p[i] = int(data[i])

    # Fenwick tree over slots 1..n, all initially free (value 1).
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)

    res = [0] * (n + 1)
    LOG = 1
    while LOG * 2 <= n:
        LOG *= 2

    for i in range(n, 0, -1):
        k = p[i]
        pos = 0
        step = LOG
        while step:
            nxt = pos + step
            if nxt <= n and tree[nxt] < k:
                pos = nxt
                k -= tree[nxt]
            step >>= 1
        slot = pos + 1
        res[slot] = i
        j = slot
        while j <= n:
            tree[j] -= 1
            j += j & (-j)

    sys.stdout.write(" ".join(map(str, res[1:])) + "\n")


if __name__ == "__main__":
    main()
