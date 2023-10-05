a = int(input("Enter a number: "))
b = int(input("Enter another number to be added/subtracted to/from the first: "))
c = input("Enter an operator (either + or -): ")

if c == "+":
    print("The sum of these numbers is " + str(a+b))
elif c == "-":
    print("The difference of these numbers is " + str(a-b))
else:
    print("Unknown operator")