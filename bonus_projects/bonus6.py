contents = [
    "All carrots to be sliced longitudinally",
    "The carrots were reported sliced",
    "The carrots were sliced again",
]

filenames = ["doc.txt", "report.txt", "presentation.txt"]

for content, filename in zip(contents, filenames):
    file = open(f"./files/{filename}", "w")
    file.write(content)
    file.close()
