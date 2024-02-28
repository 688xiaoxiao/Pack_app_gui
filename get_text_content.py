with open('selections.txt', 'r') as file:
    content = file.read()

lines = content.split('\n')

for line in lines:
    if line.startswith('left='):
        left_value = line.split('=')[1]
    elif line.startswith('right='):
        right_value = line.split('=')[1]

print('Left:', left_value, end='|')
print('Right:', right_value, end='|')