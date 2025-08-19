password = input("Enter password: ")

while password != "pass123":
    password = input("Enter password: ")

print("Password is correct")

#######################################################

user_names = []

user_input = input("Enter your name: ")

while user_input != "exit":
    print(user_input)
    user_input = user_input.capitalize()
    user_names.append(user_input)
    user_input = input("Enter your name: ")
