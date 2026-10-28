# Write your solution here. Read from stdin, write to stdout.

import sys
from collections import deque

def get_neighbors(state, N):
    L = N + 2
    e = state.find('..')  # position of empty pair start
    # generate moves swapping empty pair with any adjacent occupied pair
    lst = list(state)
    for x in range(L - 1):
        if x == e:
            continue
        if lst[x] != '.' and lst[x+1] != '.':
            nxt = lst.copy()
            # move pair to empty location
            nxt[e] = lst[x]
            nxt[e+1] = lst[x+1]
            # empty moves to former pair location
            nxt[x] = '.'
            nxt[x+1] = '.'
            yield ''.join(nxt)

def bidirectional_bfs(start, goal, N):
    if start == goal:
        return 0
    # frontiers
    front_f = {start: 0}
    front_b = {goal: 0}
    q_f = deque([start])
    q_b = deque([goal])
    L = N + 2
    while q_f and q_b:
        # expand the smaller frontier
        if len(q_f) <= len(q_b):
            q = q_f
            visited_cur = front_f
            visited_opp = front_b
        else:
            q = q_b
            visited_cur = front_b
            visited_opp = front_f
        for _ in range(len(q)):
            cur = q.popleft()
            d = visited_cur[cur]
            for nxt in get_neighbors(cur, N):
                if nxt in visited_cur:
                    continue
                if nxt in visited_opp:
                    return d + 1 + visited_opp[nxt]
                visited_cur[nxt] = d + 1
                q.append(nxt)
    return -1

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    start = S + ".."
    goal = T + ".."
    ans = bidirectional_bfs(start, goal, N)
    print(ans)

if __name__ == "__main__":
    solve()
