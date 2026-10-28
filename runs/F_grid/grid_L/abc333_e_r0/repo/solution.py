import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = [0] * n
    x = [0] * n
    for i in range(n):
        t[i] = int(data[1 + 2 * i])
        x[i] = int(data[2 + 2 * i])

    stacks = [[] for _ in range(n + 1)]  # unpicked potion indices per type
    held = [0] * (n + 1)                 # picked-but-unconsumed per type
    pick = [0] * n

    for i in range(n):
        xi = x[i]
        if t[i] == 1:
            stacks[xi].append(i)
        else:
            if held[xi] == 0:
                st = stacks[xi]
                if not st:
                    print(-1)
                    return
                j = st.pop()  # latest unpicked potion of this type
                pick[j] = 1
                held[xi] += 1
            held[xi] -= 1

    cur = 0
    best = 0
    for i in range(n):
        if t[i] == 1:
            cur += pick[i]
        else:
            cur -= 1
        if cur > best:
            best = cur

    out = [str(best), " ".join(str(pick[i]) for i in range(n) if t[i] == 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
