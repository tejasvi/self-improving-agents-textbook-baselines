MOD = 998244353


def is_good_string(s):
    """Check if a string is a good string using BFS."""
    if len(s) == 0:
        return True
    
    from collections import deque
    
    visited = set()
    queue = deque([s])
    visited.add(s)
    
    while queue:
        curr = queue.popleft()
        
        if len(curr) == 0:
            return True
        
        count_a = curr.count('A')
        count_b = curr.count('B')
        count_c = curr.count('C')
        
        # Try operation 1: remove two identical characters
        for i in range(len(curr)):
            for j in range(i + 1, len(curr)):
                if curr[i] == curr[j]:
                    new_s = curr[:i] + curr[i+1:j] + curr[j+1:]
                    if new_s not in visited:
                        visited.add(new_s)
                        queue.append(new_s)
        
        # Try operation 2: remove one A, one B, one C
        if count_a >= 1 and count_b >= 1 and count_c >= 1:
            a_idx = curr.index('A')
            b_idx = curr.index('B')
            c_idx = curr.index('C')
            
            indices_to_remove = sorted([a_idx, b_idx, c_idx], reverse=True)
            new_s = curr
            for idx in indices_to_remove:
                new_s = new_s[:idx] + new_s[idx+1:]
            
            if new_s not in visited:
                visited.add(new_s)
                queue.append(new_s)
    
    return False


def solve():
    n, k = map(int, input().split())
    s = input().strip()
    
    # Find positions of '?'
    question_positions = [i for i, c in enumerate(s) if c == '?']
    num_questions = len(question_positions)
    
    # Generate all possible replacements
    result = 0
    
    for mask in range(3 ** num_questions):
        # Replace '?' with characters based on mask
        s_list = list(s)
        temp_mask = mask
        for pos in question_positions:
            char_idx = temp_mask % 3
            s_list[pos] = ['A', 'B', 'C'][char_idx]
            temp_mask //= 3
        
        s_replaced = ''.join(s_list)
        
        # Count good substrings
        good_count = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                substring = s_replaced[i:j]
                if is_good_string(substring):
                    good_count += 1
        
        if good_count >= k:
            result = (result + 1) % MOD
    
    print(result)


if __name__ == "__main__":
    solve()
