import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = 2 * n
    partner = [0] * (m + 1)
    for i in range(n):
        a = int(data[1 + 2 * i])
        b = int(data[2 + 2 * i])
        partner[a] = b
        partner[b] = a
    stack = []
    for p in range(1, m + 1):
        q = partner[p]
        if q > p:
            stack.append(p)
        else:
            if not stack or stack[-1] != q:
                print("Yes")
                return
            stack.pop()
    print("No")


main()
