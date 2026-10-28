import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    c0 = 0  # number of starts i<=j with f(i,j)=0
    c1 = 0  # number of starts i<=j with f(i,j)=1
    total = 0
    for j in range(1, n + 1):
        if s[j - 1] == '0':
            # all earlier results become 1; new start gives 0
            c0, c1 = 1, j - 1
        else:
            # NAND with 1 flips every earlier result; new start gives 1
            c0, c1 = c1, c0 + 1
        total += c1
    print(total)


main()
