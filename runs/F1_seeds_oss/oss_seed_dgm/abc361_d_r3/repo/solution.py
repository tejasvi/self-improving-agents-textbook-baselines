# Write your solution here. Read from stdin, write to stdout.

import sys
from collections import deque

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    start = S + '..'
    target = T + '..'
    if start == target:
        print(0)
        return
    # BFS
    q = deque([start])
    dist = {start: 0}
    while q:
        cur = q.popleft()
        d = dist[cur]
        # locate blanks
        blank_idx = cur.find('..')  # there is exactly one pair
        # try moving any adjacent occupied pair
        for i in range(N+1):  # positions 0..N (since length N+2, last pair start N+1? Actually last index is N+1, but we need i,i+1 within range
            if i == blank_idx:
                continue  # this is the blank pair itself
            if cur[i] != '.' and cur[i+1] != '.':
                # move pair i,i+1 to blanks
                lst = list(cur)
                # place stones at blanks
                lst[blank_idx] = cur[i]
                lst[blank_idx+1] = cur[i+1]
                # make original positions blanks
                lst[i] = '.'
                lst[i+1] = '.'
                nxt = ''.join(lst)
                if nxt not in dist:
                    if nxt == target:
                        print(d+1)
                        return
                    dist[nxt] = d+1
                    q.append(nxt)
    print(-1)

if __name__ == "__main__":
    solve()
