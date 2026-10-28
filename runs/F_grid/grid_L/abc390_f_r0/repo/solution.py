import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    pos = [[] for _ in range(n + 2)]
    for i in range(n):
        pos[int(a[i])].append(i + 1)  # 1-indexed positions

    def G(lists):
        # sum over maximal segments avoiding all forbidden positions (merged sorted lists)
        merged = sorted(set().union(*lists)) if len(lists) > 1 else lists[0]
        total = 0
        prev = 0
        for p in merged:
            g = p - prev - 1
            total += g * (g + 1) // 2
            prev = p
        g = n - prev
        total += g * (g + 1) // 2
        return total

    ans = 0
    for v in range(1, n + 1):
        if not pos[v]:
            continue
        pm = pos[v - 1] if v - 1 >= 1 else []
        # subarrays containing v and avoiding v-1
        ans += G([pm]) - G([pm, pos[v]])
    print(ans)

main()
