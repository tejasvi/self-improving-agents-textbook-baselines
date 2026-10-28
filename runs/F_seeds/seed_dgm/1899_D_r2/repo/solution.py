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
        cnt = Counter(int(tok) for tok in data[pos:pos + n])
        pos += n
        # b_i^{b_j} = b_j^{b_i}  <=>  a_i / 2^{a_i} == a_j / 2^{a_j}.
        # f(x) = x / 2^x is injective except f(1) = f(2).
        ans = 0
        for c in cnt.values():
            ans += c * (c - 1) // 2
        ans += cnt.get(1, 0) * cnt.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
