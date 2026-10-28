import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    # c0[i]: min flips to make leaf i equal 0; c1[i]: to make it 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 if ch == '0' else 0 for ch in s]
    for _ in range(n):
        m = len(c0) // 3
        n0 = [0] * m
        n1 = [0] * m
        for i in range(m):
            j = 3 * i
            x, y, z = c0[j], c0[j + 1], c0[j + 2]
            n0[i] = x + y + z - max(x, y, z)
            x, y, z = c1[j], c1[j + 1], c1[j + 2]
            n1[i] = x + y + z - max(x, y, z)
        c0, c1 = n0, n1
    # root's current value is the one that costs 0 to achieve
    if c0[0] == 0:
        ans = c1[0]
    else:
        ans = c0[0]
    print(ans)

main()
