import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # a_i: longest prefix of T obtained greedily as a subsequence of S_i
    # b_j: longest suffix of T obtained greedily (from the right) as a subsequence of S_j
    cnt_b = [0] * (m + 2)
    a_list = []
    for s in strs:
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a_list.append(p)

        q = m
        for c in reversed(s):
            if q > 0 and t[q - 1] == c:
                q -= 1
        cnt_b[m - q] += 1

    # suffix sums: ge[k] = number of j with b_j >= k
    ge = [0] * (m + 2)
    acc = 0
    for k in range(m, -1, -1):
        acc += cnt_b[k]
        ge[k] = acc

    ans = 0
    for a in a_list:
        need = m - a
        if need < 0:
            need = 0
        ans += ge[need]
    print(ans)


main()
