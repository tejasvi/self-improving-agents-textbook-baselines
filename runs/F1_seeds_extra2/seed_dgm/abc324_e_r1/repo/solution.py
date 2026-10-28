import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # a_i: greedy matched prefix length of T within S_i
    # b_j: greedy matched suffix length of T within S_j
    a_vals = [0] * n
    cnt_b = [0] * (m + 2)
    for idx, s in enumerate(strs):
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a_vals[idx] = p

        q = 0
        for c in reversed(s):
            if q < m and t[m - 1 - q] == c:
                q += 1
        cnt_b[q] += 1

    # suf[k] = number of j with b_j >= k
    suf = [0] * (m + 2)
    running = 0
    for k in range(m, -1, -1):
        running += cnt_b[k]
        suf[k] = running

    ans = 0
    for a in a_vals:
        need = m - a
        if need < 0:
            need = 0
        ans += suf[need]

    print(ans)


main()
