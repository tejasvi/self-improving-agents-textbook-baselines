import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    # For each value, positions p_0<p_1<...; with q_t = p_t - t,
    # the number of valid triples with the pair (a, b), a<b, equals q_b - q_a.
    cnt = defaultdict(int)     # number of occurrences seen so far
    qsum = defaultdict(int)    # sum of q_a over occurrences seen so far
    total = 0
    for p, v in enumerate(a):
        t = cnt[v]
        q = p - t
        total += t * q - qsum[v]
        qsum[v] += q
        cnt[v] = t + 1
    print(total)


main()
