import sys


def main():
    s = sys.stdin.readline().strip()
    stack = []
    for ch in s:
        stack.append(ch)
        if len(stack) >= 3 and stack[-3] == 'A' and stack[-2] == 'B' and stack[-1] == 'C':
            del stack[-3:]
    sys.stdout.write(''.join(stack) + "\n")


if __name__ == "__main__":
    main()
