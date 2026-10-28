import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # p[i]: longest prefix of T that is a subsequence of S_i
    # s[j]: longest suffix of T that is a subsequence of S_j
    p_list = []
    cnt_s = [0] * (m + 2)
    for st in strs:
        p = 0
        for c in st:
            if p < m and t[p] == c:
                p += 1
        p_list.append(p)

        q = m - 1
        for c in reversed(st):
            if q >= 0 and t[q] == c:
                q -= 1
        cnt_s[m - 1 - q] += 1

    # suffix sums: ge[k] = number of j with s_j >= k
    ge = [0] * (m + 2)
    for k in range(m, -1, -1):
        ge[k] = ge[k + 1] + cnt_s[k]

    ans = 0
    for p in p_list:
        need = m - p
        if need <= 0:
            ans += n
        else:
            ans += ge[need]
    print(ans)


if __name__ == "__main__":
    main()
