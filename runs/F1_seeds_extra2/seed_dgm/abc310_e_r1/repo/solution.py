import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()[:n]
    c0 = 0  # number of starts i <= j with f(i,j) == 0
    c1 = 0  # number of starts i <= j with f(i,j) == 1
    total = 0
    for ch in s:
        if ch == '0':
            # NAND with 0 always yields 1
            c1 = c0 + c1
            c0 = 0
            # new start i=j with value 0
            c0 += 1
        else:
            # NAND with 1 flips the value
            c0, c1 = c1, c0
            # new start i=j with value 1
            c1 += 1
        total += c1
    print(total)


main()
