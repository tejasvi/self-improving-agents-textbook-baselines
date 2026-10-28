import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    p = [int(x) for x in data[1:1 + n]]

    # Process insertions in reverse. Element i takes the P_i-th slot that is
    # still free among positions 1..N. A Fenwick tree over free slots supports
    # finding the k-th free slot and removing it in O(log N).
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)  # all positions initially free

    log = 1
    while log * 2 <= n:
        log *= 2

    ans = [0] * (n + 1)
    for i in range(n, 0, -1):
        k = p[i - 1]
        pos = 0
        step = log
        while step:
            nxt = pos + step
            if nxt <= n and tree[nxt] < k:
                pos = nxt
                k -= tree[nxt]
            step >>= 1
        pos += 1
        ans[pos] = i
        j = pos
        while j <= n:
            tree[j] -= 1
            j += j & (-j)

    sys.stdout.write(" ".join(map(str, ans[1:])) + "\n")


main()
