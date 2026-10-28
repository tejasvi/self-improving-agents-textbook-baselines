import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    # Positions of ones (0-indexed); after moving the j-th one (0-indexed)
    # to its target t+j, the cost is |(p_j - j) - t|. Minimize over t via median.
    a = []
    j = 0
    for i, c in enumerate(s):
        if c == '1':
            a.append(i - j)
            j += 1
    m = a[len(a) // 2]
    print(sum(abs(x - m) for x in a))


if __name__ == "__main__":
    main()
