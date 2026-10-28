import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    # c0: number of starts i<=j with f(i,j)=0; c1: with f(i,j)=1
    c0 = 0
    c1 = 0
    ans = 0
    for ch in s:
        if ch == '0':
            # every existing chain becomes 1; new start gives 0
            c1, c0 = c0 + c1, 1
        else:
            # existing: 0 -> 1, 1 -> 0; new start gives 1
            c1, c0 = c0 + 1, c1
        ans += c1
    print(ans)


if __name__ == "__main__":
    main()
