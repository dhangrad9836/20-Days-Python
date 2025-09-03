"""
For this exercise, download the members.txt file attached to the resources. Then, create a program that:
1. prompts the user to enter a new member.
2. adds that member to members.txt at the end of the existing members. For example, the user here has entered the member Solomon Right.
In the above example, Solomon Right will be added to members.txt updating the content of the file to:
John Smith

Sen Lakmi

Sono Octonot

Solomon Right
"""

# prompt for the user to enter a member name
new_member = input("Enter a new member: ") + "\n"

# open the members.txt file in read mode
file = open("members.txt", "r")

# store the contents of the members.txt file in the members_file variable as a list using readlines()
members_file = file.readlines()

# close the file after reading it
file.close()

# append the new member to the list members_file
members_file.append(new_member)

# create a new file called file, open the txt file and label is as w for write which will overwrite the existing file
file = open("members.txt", "w")

# here we will write the list of the new members with writelines() to the file with the old contents and the new member added
members_file = file.writelines(members_file)
# close the file after writing to it
file.close()


#   # create a new file called file, open the txt file and label is as w for write which will overwrite the existing file
#             file = open("todos.txt", "w")

#             # here we will write the list of the new todos with writelines()  to the file with the old conents and the new todo added
#             file.writelines(todos)
#             file.close()  # close the file after writing to it
