import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos])
        pos += 1
        cnt = Counter(data[pos:pos + n])
        pos += n
        # Keys are byte strings; normalise to ints for comparison.
        c = {}
        for k, v in cnt.items():
            c[int(k)] = v
        # Condition reduces to a_i / 2^{a_i} == a_j / 2^{a_j}.
        # f(1) == f(2) = 1/2, and f is strictly decreasing for x >= 2.
        ans = 0
        for v in c.values():
            ans += v * (v - 1) // 2
        ans += c.get(1, 0) * c.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
