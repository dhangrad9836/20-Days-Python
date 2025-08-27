# this script renames files by replacing the first decimal point in the filename with a hyphen

filenames = ["1.Raw Data.txt", "2.Processed Data.txt", "3.Analysis Results.txt"]

for filename in filenames:
    # use .replace to change a deciamal to hypen but only the first occurence...so you have to add 3rd arguement of 1
    filename = filename.replace(".", "-", 1)
    print(filename)


# use a tuple to store immutable data so you dont accidently change it

filename_tuple = (1, 3, 2, 3, 5, 3, 5)
print(filename_tuple)


elements = ["a", "b", "c"]
new = "x"
elements[1] = new
print(elements)
