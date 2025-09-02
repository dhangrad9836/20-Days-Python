# the text inside parentheses is called the arguement
# list we are storing todos in
# todos = []

# while statement to repeat question
while True:
    user_action = input("Type add, show, edit, complete, or exit: ")
    user_action = (
        user_action.strip()
    )  # to remove any whitespace accidently added by the user

    match user_action:
        case "add":
            # user input for stored in variable todo
            todo = input("Enter a todo: ") + "\n"

            # read in the text file and store the current contents
            file = open("todos.txt", "r")  # r is for read the file contents

            # create a new variable called todos which will store the list of todos
            # now we do a readlines to read the contents line by line hence readlines() of the file and store it as a list inside the todos variable which is defined here todos
            todos = file.readlines()
            file.close()  # close the file after reading it

            # now append the user input to the list todos
            todos.append(todo)

            # create a new file called file, open the txt file and label is as w for write which will overwrite the existing file
            file = open("todos.txt", "w")

            # here we will write the list of the new todos with writelines()  to the file with the old conents and the new todo added
            file.writelines(todos)
            file.close()  # close the file after writing to it
        case "show":
            # open the 'todos.txt' file in read mode
            file = open("todos.txt", "r")
            # store the contents of the todos.txt file in the todos variable as a list using readlines()
            todos = file.readlines()
            file.close()
            # the enumerate function gives us both the index and the item in the list
            for index, item in enumerate(todos):
                item = item.title()
                index = index + 1  # to start the index at 1 instead of 0
                # print(index, " ", item) this will print a number for each item todo
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
