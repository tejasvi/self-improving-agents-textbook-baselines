import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = 2 * n
    # partner[p] = other endpoint of the chord containing point p
    partner = [0] * (m + 1)
    for i in range(n):
        a = int(data[1 + 2 * i])
        b = int(data[2 + 2 * i])
        partner[a] = b
        partner[b] = a
    # Walk points in order; chords are non-crossing iff the sequence of
    # open/close events forms a proper nesting (stack discipline).
    stack = []
    for p in range(1, m + 1):
        q = partner[p]
        if q > p:
            stack.append(p)
        else:
            # p is the right endpoint of the chord (q, p); its left endpoint must be on top
            if stack and stack[-1] == q:
                stack.pop()
            else:
                print("Yes")
                return
    print("No")


main()
