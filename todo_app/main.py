# the text inside parentheses is called the arguement
user_prompt = "Enter a todo:"

todos = []

# while statement to repeat question
while True:
    todo = input(user_prompt)
    todos.append(todo)
    print(todos)
