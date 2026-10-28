import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0[v]/c1[v]: number of starts i <= j whose current f(i,j) is 0 / 1
    c0 = 0
    c1 = 0
    total = 0
    for ch in s:
        if ch == '0':
            # NAND with 0 gives 1 for every existing start
            c1 = c0 + c1
            c0 = 0
            # new start i=j with value 0
            c0 += 1
        else:
            # NAND with 1 negates every existing start
            c0, c1 = c1, c0
            # new start i=j with value 1
            c1 += 1
        total += c1
    print(total)


main()
