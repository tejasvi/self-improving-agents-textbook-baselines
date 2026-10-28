import math

# Read N
N = int(input())

# Determine minimum number of friends needed
# We need 2^M >= N, so M = ceil(log2(N))
M = math.ceil(math.log2(N))

# Print M
print(M)

# For each friend i (0-indexed), they get bottles where bit i is set in (j-1)
# We use bottles numbered 1 to N
# We map bottle j to index (j-1), and friend i gets bottle j if bit i is set in (j-1)

for i in range(M):
    bottles = []
    for j in range(1, N + 1):
        # Check if bit i is set in (j-1)
        if ((j - 1) >> i) & 1:
            bottles.append(j)
    
    # Print K_i followed by the bottles
    output_line = [str(len(bottles))] + [str(b) for b in bottles]
    print(' '.join(output_line))

# Read the response string
S = input().strip()

# Convert the response to a bottle number
# S[i] tells us if friend i got upset
# This gives us the binary representation of (spoiled_bottle - 1)
spoiled_index = 0
for i in range(M):
    if S[i] == '1':
        spoiled_index |= (1 << i)

# Add 1 to convert from 0-indexed to 1-indexed bottle number
spoiled_bottle = spoiled_index + 1

# Print the spoiled bottle number
print(spoiled_bottle)
