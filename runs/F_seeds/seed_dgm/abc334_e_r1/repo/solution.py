import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    MOD = 998244353
    rows = data[2:2 + H]
    W2 = W + 2
    # padded flat grid: 1 = green, 0 = red/border
    green = bytearray((H + 2) * W2)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == 35:  # '#'
                green[base + j] = 1

    label = [0] * ((H + 2) * W2)
    C = 0
    for idx in range(len(green)):
        if green[idx] and not label[idx]:
            C += 1
            label[idx] = C
            stack = [idx]
            while stack:
                v = stack.pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and not label[u]:
                        label[u] = C
                        stack.append(u)

    total = 0
    red_count = 0
    for i in range(1, H + 1):
        base = i * W2
        for j in range(1, W + 1):
            v = base + j
            if green[v]:
                continue
            red_count += 1
            s = set()
            l = label[v - 1]
            if l:
                s.add(l)
            l = label[v + 1]
            if l:
                s.add(l)
            l = label[v - W2]
            if l:
                s.add(l)
            l = label[v + W2]
            if l:
                s.add(l)
            total += C + 1 - len(s)

    ans = total % MOD * pow(red_count % MOD, MOD - 2, MOD) % MOD
    print(ans)


main()
