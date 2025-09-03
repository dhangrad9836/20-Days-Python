"""
Creating Multiple Text Files
In the coding area, we have defined a list of countries. Add some code that uses a for loop to generate a text file for each country (e.g., "Albania.txt", "Belgium.txt", and so on).

Each file should have its country name as content (e.g., Albania.txt has Albania as content).
"""

countries = ["Albania", "Belgium", "Canada", "Denmark", "Ethiopia", "France"]

# filenames = []

for country_file in countries:
    # filenames.append(country_file + end_string)
    file = open(f"{country_file}.txt", "w")
    file.write(country_file)
    file.close()  # closing the file after writing to it is important or it will read errors.
