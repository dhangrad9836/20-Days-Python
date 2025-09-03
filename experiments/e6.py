filenames = ["doc.txt", "report.txt", "presentation.txt"]

for file in filenames:
    # rember that open() with "w" will overwrite the existing file or create a new file if it does not exist
    file = open(f"{file}", "w")
    file.write("Hello")
    file.close()


# contents = [
#     "All carrots to be sliced longitudinally",
#     "The carrots were reported sliced",
#     "The carrots were sliced again",
# ]

# filenames = ["doc.txt", "report.txt", "presentation.txt"]

# for content, filename in zip(contents, filenames):
#     file = open(f"./files/{filename}", "w")
#     file.write(content)
#     file.close()
