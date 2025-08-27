waiting_list = ["sen", "ben", "john"]
waiting_list.sort(reverse=True)  # sort in descending order

for index, item in enumerate(waiting_list):
    row = f"{index+1}.{item.capitalize()}"
    print(row)


# menu = ["pasta", "pizza", "salad"]

# user_choice = int(input("Enter the index of the item: "))

# message = f"You chose {menu[user_choice]}."
# print(message)


# menu = ["pasta", "pizza", "salad"]

# for i, j in enumerate(menu):
#     print(f"{i}.{j}")


menu = ["pasta", "pizza", "salad"]

for i, j in enumerate(menu):
    print(f"{i}.{j}")
