import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    people = []
    for i in range(n):
        a = int(data[1 + 2 * i])
        b = int(data[2 + 2 * i])
        people.append((a, b))
    S = sum(b for _, b in people)
    if S % 3 != 0:
        print(-1)
        return
    T = S // 3
    INF = 10 ** 9
    # dp[s1][s2] = min number of switches so that team1 sum = s1, team2 sum = s2,
    # with team3 sum = (processed total - s1 - s2). All sums capped at T.
    dp = [[INF] * (T + 1) for _ in range(T + 1)]
    dp[0][0] = 0
    for a, b in people:
        c = [0 if a == 1 else 1, 0 if a == 2 else 1, 0 if a == 3 else 1]
        c1, c2, c3 = c
        new = [[INF] * (T + 1) for _ in range(T + 1)]
        for s1 in range(T + 1):
            row = dp[s1]
            if all(x >= INF for x in row):
                continue
            # person joins team 3: stays in same s1, s2
            cur = new[s1]
            new[s1] = list(map(min, cur, [x + c3 for x in row]))
            # person joins team 2: s2 -> s2 + b
            if b <= T:
                shifted = [INF] * b + [x + c2 for x in row[:T + 1 - b]]
                new[s1] = list(map(min, new[s1], shifted))
            # person joins team 1: s1 -> s1 + b
            if s1 + b <= T:
                t = s1 + b
                new[t] = list(map(min, new[t], [x + c1 for x in row]))
        dp = new
    ans = dp[T][T]
    print(ans if ans < INF else -1)


main()
