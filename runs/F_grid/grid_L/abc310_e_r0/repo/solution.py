import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    c0 = 0  # number of starts i with f(i,j) == 0
    c1 = 0  # number of starts i with f(i,j) == 1
    total = 0
    for ch in s:
        if ch == '0':
            # x NAND 0 = 1 for all x; new single element is 0
            c1 = c0 + c1
            c0 = 1
        else:
            # x NAND 1 = NOT x; new single element is 1
            c0, c1 = c1, c0 + 1
        total += c1
    print(total)


main()
