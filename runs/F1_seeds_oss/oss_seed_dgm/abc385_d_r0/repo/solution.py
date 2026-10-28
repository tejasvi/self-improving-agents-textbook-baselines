# Write your solution here. Read from stdin, write to stdout.
import sys, bisect

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))
    # Fixed coordinate -> list of (variable coordinate, house index), sorted
    x_dict = {}
    y_dict = {}
    for idx in range(N):
        x = int(next(it))
        y = int(next(it))
        x_dict.setdefault(x, []).append((y, idx))
        y_dict.setdefault(y, []).append((x, idx))
    for lst in x_dict.values():
        lst.sort(key=lambda p: p[0])
    for lst in y_dict.values():
        lst.sort(key=lambda p: p[0])
    visited = [False] * N
    cnt = 0
    cur_x, cur_y = Sx, Sy

    def visit_range(coord_map, key, lo, hi):
        """Visit houses on line with fixed coordinate `key` whose variable coordinate lies in [lo, hi].
        Houses are marked visited only once and removed from the list to keep total work O(N).
        Returns number of newly visited houses.
        """
        lst = coord_map.get(key)
        if not lst:
            return 0
        if lo > hi:
            lo, hi = hi, lo
        left = bisect.bisect_left(lst, (lo, -1))
        added = 0
        # iterate while within range; pop visited elements to avoid future checks
        while left < len(lst) and lst[left][0] <= hi:
            var, idx = lst[left]
            if not visited[idx]:
                visited[idx] = True
                added += 1
            # remove this entry regardless (it is now visited)
            lst.pop(left)
            # do not increment left because list shifts
        return added

    for _ in range(M):
        d = next(it).decode()
        c = int(next(it))
        if d == 'U':
            new_y = cur_y + c
            cnt += visit_range(x_dict, cur_x, cur_y, new_y)
            cur_y = new_y
        elif d == 'D':
            new_y = cur_y - c
            cnt += visit_range(x_dict, cur_x, cur_y, new_y)
            cur_y = new_y
        elif d == 'R':
            new_x = cur_x + c
            cnt += visit_range(y_dict, cur_y, cur_x, new_x)
            cur_x = new_x
        else:  # 'L'
            new_x = cur_x - c
            cnt += visit_range(y_dict, cur_y, cur_x, new_x)
            cur_x = new_x
    sys.stdout.write(f"{cur_x} {cur_y} {cnt}\n")

if __name__ == "__main__":
    main()
