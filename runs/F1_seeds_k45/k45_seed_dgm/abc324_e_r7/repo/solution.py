def is_subsequence(text, pattern):
    """Check if pattern is a subsequence of text"""
    pattern_idx = 0
    for char in text:
        if pattern_idx < len(pattern) and char == pattern[pattern_idx]:
            pattern_idx += 1
    return pattern_idx == len(pattern)

def main():
    first_line = input().split()
    N = int(first_line[0])
    T = first_line[1]
    
    strings = []
    for _ in range(N):
        strings.append(input().strip())
    
    count = 0
    for i in range(N):
        for j in range(N):
            concatenated = strings[i] + strings[j]
            if is_subsequence(concatenated, T):
                count += 1
    
    print(count)

if __name__ == "__main__":
    main()
