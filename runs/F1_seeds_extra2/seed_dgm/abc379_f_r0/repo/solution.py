import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    H = [int(x) for x in data[2:2 + n]]

    # nge[i]: nearest j > i with H[j] > H[i], else n
    nge = [n] * (n + 1)
    st = []
    for i in range(n):
        h = H[i]
        while st and H[st[-1]] < h:
            nge[st.pop()] = i
        st.append(i)
    # depth[i]: number of elements in the next-greater chain starting at i
    depth = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        depth[i] = 1 + depth[nge[i]]

    # sparse table of argmax (H values are distinct)
    table = [list(range(n))]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        cur = []
        for i in range(n - (1 << j) + 1):
            a = prev[i]
            b = prev[i + half]
            cur.append(a if H[a] > H[b] else b)
        table.append(cur)
        j += 1

    out = []
    pos = 2 + n
    for _ in range(q):
        l = int(data[pos]) - 1
        r = int(data[pos + 1]) - 1
        pos += 2
        lev = (r - l + 1).bit_length() - 1
        t = table[lev]
        a = t[l]
        b = t[r - (1 << lev) + 1]
        p = a if H[a] > H[b] else b
        out.append(depth[nge[p]])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
