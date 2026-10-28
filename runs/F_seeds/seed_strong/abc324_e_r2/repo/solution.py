import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # a_i: longest prefix of T that is a subsequence of S_i
    # b_j: longest suffix of T that is a subsequence of S_j
    cnt_b = [0] * (m + 2)
    a_vals = []
    for s in strs:
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a_vals.append(p)
        q = m - 1
        for c in reversed(s):
            if q >= 0 and t[q] == c:
                q -= 1
        cnt_b[m - 1 - q] += 1

    # suffix sums: suf[k] = number of j with b_j >= k
    suf = [0] * (m + 2)
    for k in range(m, -1, -1):
        suf[k] = suf[k + 1] + cnt_b[k]

    ans = 0
    for a in a_vals:
        need = m - a
        if need <= 0:
            ans += n
        else:
            ans += suf[need]
    print(ans)

main()
