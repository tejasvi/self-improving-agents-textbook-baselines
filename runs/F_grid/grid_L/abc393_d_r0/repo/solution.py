import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    # q_j = position of j-th one (0-indexed) minus j; nondecreasing.
    q = []
    j = 0
    for i, c in enumerate(s):
        if c == '1':
            q.append(i - j)
            j += 1
    med = q[len(q) // 2]
    print(sum(abs(x - med) for x in q))


main()
