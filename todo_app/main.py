# the text inside parentheses is called the arguement

todos = []

# while statement to repeat question
while True:
    user_action = input("Type add, show, or exit: ")
    user_action = (
        user_action.strip()
    )  # to remove any whitespace accidently added by the user

    match user_action:
        case "add":
            todo = input("Enter a todo: ")
            todos.append(todo)
        case "show":
            for item in todos:
                item = item.title()
                print(item)
        case "exit":
            break

print("bye")
