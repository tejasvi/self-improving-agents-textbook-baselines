import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    # For each value v with positions p_0<p_1<...: count of j between a pair
    # (p_a, p_b) with A_j != v equals (p_b - b) - (p_a - a) where q_t = p_t - t.
    # Sum over pairs a<b of (q_b - q_a), computed with running sums.
    cnt = {}
    sums = {}
    total = 0
    for pos in range(n):
        v = a[pos]
        c = cnt.get(v, 0)  # number of previous occurrences (index b)
        q = pos - c        # q_b = p_b - b (0-indexed positions)
        s = sums.get(v, 0)  # sum of q_a for earlier occurrences
        total += c * q - s
        sums[v] = s + q
        cnt[v] = c + 1
    print(total)


main()
