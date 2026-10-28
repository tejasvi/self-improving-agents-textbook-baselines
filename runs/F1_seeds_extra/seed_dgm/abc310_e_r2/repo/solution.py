import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    c0 = 0  # number of start positions i with f(i,j) == 0
    c1 = 0  # number of start positions i with f(i,j) == 1
    total = 0
    for j in range(n):
        if s[j] == '0':
            # all existing values become 1 (x NAND 0 = 1)
            c1 = j
            c0 = 1  # new start f(j,j) = 0
        else:
            # x NAND 1 = NOT x: swap counts
            c0, c1 = c1, c0
            c1 += 1  # new start f(j,j) = 1
        total += c1
    print(total)


main()
