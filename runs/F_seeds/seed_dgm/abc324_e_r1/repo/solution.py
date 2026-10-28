import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    T = data[1]
    m = len(T)
    S = data[2:2 + n]

    # a_i: longest prefix of T that is a subsequence of S_i (greedy)
    a_vals = [0] * n
    for idx in range(n):
        p = 0
        for c in S[idx]:
            if p < m and T[p] == c:
                p += 1
        a_vals[idx] = p

    # b_j: longest suffix of T that is a subsequence of S_j (greedy from end)
    freq = [0] * (m + 2)
    for idx in range(n):
        q = m - 1
        for c in reversed(S[idx]):
            if q >= 0 and T[q] == c:
                q -= 1
        freq[m - 1 - q] += 1

    # ge[v] = number of j with b_j >= v
    ge = [0] * (m + 2)
    running = 0
    for v in range(m, -1, -1):
        running += freq[v]
        ge[v] = running

    ans = 0
    for a in a_vals:
        ans += ge[m - a]
    print(ans)


main()
