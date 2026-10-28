import math

# Read the number of bottles
N = int(input())

# Calculate minimum number of friends needed (ceiling of log2(N))
M = math.ceil(math.log2(N))

# Print the number of friends
print(M)

# For each friend i (0-indexed), we give them all bottles whose i-th bit is 1
# in the binary representation of the bottle number
# Bottles are numbered 1 to N

for friend_idx in range(M):
    bottles = []
    for bottle_num in range(1, N + 1):
        # Check if the friend_idx-th bit is set in bottle_num
        # We use LSB as bit 0
        if (bottle_num >> friend_idx) & 1:
            bottles.append(bottle_num)
    
    # Print the distribution for this friend
    print(len(bottles), *bottles)

# Read the results (which friends got sick)
S = input()

# Reconstruct the bottle number from the sick pattern
# S[i] = '1' means friend i got sick, so bit i should be set
spoiled_bottle = 0
for friend_idx in range(M):
    if S[friend_idx] == '1':
        spoiled_bottle |= (1 << friend_idx)

# Print the answer
print(spoiled_bottle)
