# the text inside parentheses is called the arguement
# list we are storing todos in
todos = []

# while statement to repeat question
while True:
    user_action = input("Type add, show, edit, complete, or exit: ")
    user_action = (
        user_action.strip()
    )  # to remove any whitespace accidently added by the user

    match user_action:
        case "add":
            todo = input("Enter a todo: ")
            todos.append(todo)
        case "show":
            # the enumerate function gives us both the index and the item in the list
            for index, item in enumerate(todos):
                item = item.title()
                index = index + 1  # to start the index at 1 instead of 0
                # print(index, " ", item)
                print(f"{index}-{item}")
        case "edit":
            number = int(input("Number of the todo to edit: "))
            # we need to subtract 1 from number so the index is correct
            number = number - 1
            new_todo = input("Enter new todo: ")
            # update the todo by overwriting the todo at that index
            todos[number] = new_todo
        case "complete":
            number = int(input("Number of the todo to complete: "))
            todos.pop(number - 1)  # subtract 1 to get correct index

        case "exit":
            break

print("bye")
