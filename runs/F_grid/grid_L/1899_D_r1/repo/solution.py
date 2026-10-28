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
        a = data[pos:pos + n]
        pos += n
        cnt = Counter(int(x) for x in a)
        # b_i^{b_j} = b_j^{b_i}  <=>  a_i / 2^{a_i} = a_j / 2^{a_j}
        # f(x) = x/2^x is equal for x=1 and x=2, otherwise strictly decreasing.
        ans = 0
        for v in cnt.values():
            ans += v * (v - 1) // 2
        ans += cnt.get(1, 0) * cnt.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
