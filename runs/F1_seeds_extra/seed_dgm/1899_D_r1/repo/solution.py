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
        # Compare values as integers.
        cnt = Counter(int(tok) for tok in data[pos:pos + n])
        pos += n
        # b_i^{b_j} = b_j^{b_i} <=> a_i / 2^{a_i} == a_j / 2^{a_j}.
        # x / 2^x is equal for x = 1 and x = 2 only, otherwise injective.
        ans = 0
        for v in cnt.values():
            ans += v * (v - 1) // 2
        ans += cnt.get(1, 0) * cnt.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
