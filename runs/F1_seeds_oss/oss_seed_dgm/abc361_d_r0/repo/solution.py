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
    # Represent configuration as a string of length N+2, with '.' for empty cells
    start = S + '..'
    target = T + '..'
    if start == target:
        print(0)
        return
    # BFS over configurations; the empty block is always contiguous '..'
    q = deque([start])
    dist = {start: 0}
    length = N + 2
    while q:
        cur = q.popleft()
        d = dist[cur]
        empty_idx = cur.find('..')  # index of the first empty cell
        # Try moving any adjacent pair of stones (i, i+1) where i != empty_idx
        for i in range(length - 1):
            if i == empty_idx:
                continue  # this is the empty block itself
            # Ensure positions i and i+1 are both stones (not empty)
            if cur[i] == '.' or cur[i+1] == '.':
                continue
            # Perform the move: stones at i,i+1 go to empty_idx, empty moves to i,i+1
            lst = list(cur)
            lst[empty_idx] = cur[i]
            lst[empty_idx + 1] = cur[i+1]
            lst[i] = '.'
            lst[i + 1] = '.'
            nxt = ''.join(lst)
            if nxt not in dist:
                if nxt == target:
                    print(d + 1)
                    return
                dist[nxt] = d + 1
                q.append(nxt)
    # If BFS finishes without reaching target, impossible
    print(-1)

if __name__ == "__main__":
    solve()
