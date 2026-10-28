from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Check if transformation is possible at all (count of W and B must match)
    if sorted(S) != sorted(T):
        print(-1)
        return
    
    # Create initial state: stones in positions 0 to N-1, empty at N and N+1
    initial_state = tuple(list(S) + ['.', '.'])
    target_state = tuple(list(T) + ['.', '.'])
    
    if initial_state == target_state:
        print(0)
        return
    
    # BFS to find minimum moves
    visited = {initial_state}
    queue = deque([(initial_state, 0)])  # (state, num_moves)
    
    while queue:
        state, moves = queue.popleft()
        
        # Generate all possible next states
        state_list = list(state)
        
        # Find empty cells
        empty_positions = []
        for i in range(N + 2):
            if state_list[i] == '.':
                empty_positions.append(i)
        
        # We must have exactly 2 empty cells
        if len(empty_positions) != 2:
            continue
        
        # Check if empty cells are adjacent
        empty_pos1, empty_pos2 = empty_positions
        if empty_pos1 > empty_pos2:
            empty_pos1, empty_pos2 = empty_pos2, empty_pos1
        
        # Try moving each pair of adjacent stones to the empty positions
        for x in range(N + 1):
            # Check if cells x and x+1 both contain stones
            if x < N + 2 and x + 1 < N + 2:
                if state_list[x] != '.' and state_list[x + 1] != '.':
                    # Create new state by swapping
                    new_state_list = state_list[:]
                    
                    # Move stones from x, x+1 to empty_pos1, empty_pos2
                    stone1 = new_state_list[x]
                    stone2 = new_state_list[x + 1]
                    new_state_list[x] = '.'
                    new_state_list[x + 1] = '.'
                    new_state_list[empty_pos1] = stone1
                    new_state_list[empty_pos2] = stone2
                    
                    new_state = tuple(new_state_list)
                    
                    if new_state == target_state:
                        print(moves + 1)
                        return
                    
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, moves + 1))
    
    print(-1)

solve()
