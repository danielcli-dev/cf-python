numbers = []
for i in range(50,101):
    numbers.append(str(i))

with open('number_list.txt', 'w') as my_file:
    my_file.writelines(numbers)