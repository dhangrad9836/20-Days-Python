# the text inside parentheses is called the arguement

todos = []

# while statement to repeat question
while True:
    user_action = input("Type add, show, or exit: ")

    match user_action:
        case "add":
            todo = input("Enter a todo: ")
            todos.append(todo)
        case "show":
            print(todos)
        case "exit":
            break

print("bye")
