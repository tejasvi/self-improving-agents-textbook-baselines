import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0, c1: number of start indices i (<= current j) whose f(i,j) is 0 / 1
    c0 = 0
    c1 = 0
    total = 0
    for j in range(n):
        if s[j] == '0':
            # all existing values become 1; new start has value 0
            c1 = j
            c0 = 1
        else:
            # existing values flip; new start has value 1
            c0, c1 = c1, c0 + 1
        total += c1
    print(total)


if __name__ == "__main__":
    main()
