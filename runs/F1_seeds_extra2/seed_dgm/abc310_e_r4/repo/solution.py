import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0: number of start indices i (<= j) with f(i,j) == 0
    # c1: number of start indices i (<= j) with f(i,j) == 1
    c0 = 0
    c1 = 0
    total = 0
    for ch in s[:n]:
        if ch == '0':
            # NAND(v, 0) = 1 for all existing starts
            c1 = c0 + c1
            c0 = 0
            # new start with value 0
            c0 += 1
        else:
            # NAND(v, 1) = NOT v: swap counts
            c0, c1 = c1, c0
            # new start with value 1
            c1 += 1
        total += c1
    print(total)


if __name__ == "__main__":
    main()
