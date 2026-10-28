import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    c0 = 0  # number of start indices i<=j with f(i,j)=0
    c1 = 0  # number with f(i,j)=1
    total = 0
    for ch in s:
        if ch == '0':
            # all previous values NAND 0 -> 1
            c1 = c0 + c1
            c0 = 0
            c0 += 1  # new start i=j with value 0
        else:
            # NAND with 1 flips each value
            c0, c1 = c1, c0
            c1 += 1  # new start i=j with value 1
        total += c1
    print(total)


main()
