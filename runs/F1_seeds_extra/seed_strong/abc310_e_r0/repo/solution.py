import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()[:n]
    c0 = 0  # count of starts i (<= current j) with f(i,j)=0
    c1 = 0  # count with f(i,j)=1
    total = 0
    for ch in s:
        if ch == '0':
            # NAND(x,0)=1 for all x; new start value 0
            c1 = c0 + c1
            c0 = 1
        else:
            # NAND(x,1)=NOT x; swap counts; new start value 1
            c0, c1 = c1, c0
            c1 += 1
        total += c1
    print(total)


main()
