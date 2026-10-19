#----------------------- PACKAGES TO IMPORT -------------------------
# The standard set of libraries we need
import numpy as np
import matplotlib.pyplot as plt

# Make plots look a little bit more fancy
plt.style.use('fivethirtyeight')

# The standard library for data in tables
import pandas as pd
import requests

#----------------------- IMPORTANT FUNCTIONS -------------------------

#Have kept the code in for notes' sake, but updated it-
# A tiny function to read a file directly from a URL
#from urllib.request import urlopen
#urllib is a package containing several modules for working with URLs.
#urllib.request is for opening and reading URLs.
#urlopen is a function within urllib.request which just opens URLs. It is useful to download only what you need from packages.

#def read_url(url):
    #return urlopen(url).read().decode()
#read() returns specified number of bytes from a file. Default is whole file.
#decode() turns encoded text (bytes) back into a string format.
#Encoded text: b'Geeks for Geeks'
#Decoded text: Geeks for Geeks


#---------------------- RETRIEVING THE TEXT -------------------------

# Get the text for Dracula
book_url = 'https://www.gutenberg.org/cache/epub/345/pg345.txt'
response = requests.get(book_url)
book_text = response.text
#This function has been defined previously as opening the URL, reading the text, and converting it into string format.

# This line is a test to make sure the code above works. It shows the first 500 characters of the text
#print(book_text[:500])


#---------------------- ANALYSING THE TEXT -------------------------
#---------BREAKING THE TEXT INTO CHAPTERS
# Break the text into Chapters
book_chapters = book_text.split('CHAPTER ')
#.split splits a string into a list where each word is a list item.
# Here, we split the book into a list and each item on the list is one chapter
# (as defined by the separator given to the function).
# The default separator is any whitespace.

# Drop the first "Chapter" - it's the Project Gutenberg header. Slicing from 27 due to chapters being listed at start.
book_chapters = book_chapters[27:]
#List[28:] is a slice notation. This creates a new list containing all elements from the original list,
# starting from index 28 (the 29th element! Index 0 is the first element).
#This means: [start the slice at this index of the string : finish the slice at this index (if empty, go to end of text].


# Show the first few words of each chapter in a table.
chapters_table = pd.DataFrame(book_chapters, columns=['Chapters'])
print(chapters_table)


#------------------ ANALYSING CHARACTER APPEARANCES
# Count how many times the characters appear in each chapter.

#This was the code provided, but numpy.char submodule no longer receives updates, meant to use numpy.strings instead.
# counts = pd.DataFrame.from_dict({
#         'Elizabeth': np.char.count(book_chapters, 'Elizabeth'),
#         'Darcy': np.char.count(book_chapters, 'Darcy'),
#         'Lydia': np.char.count(book_chapters, 'Lydia'),
#         'Wickham': np.char.count(book_chapters, 'Wickham'),
#         'Bingley': np.char.count(book_chapters, 'Bingley'),
#         'Jane': np.char.count(book_chapters, 'Jane')},
#     )

#This is my code, lightly edited to use np.strings and draw from Dracula instead of Pride and Prejudice.
# Count how many times the characters appear in each chapter.
counts = pd.DataFrame.from_dict({ #Creates DataFrame object from dictionary by columns or index.
        'Count': np.strings.count(book_chapters, 'Count'),
        'Harker': np.strings.count(book_chapters, 'Harker'),
        'Mina': np.strings.count(book_chapters, 'Mina'),
        'Seward': np.strings.count(book_chapters, 'Seward'),
        'Helsing': np.strings.count(book_chapters, 'Helsing'),
        'Quincey': np.strings.count(book_chapters, 'Quincey')},
    )
counts.head()

#classmethod DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)
#data = dict (should be {field: array-like} or {field:dict})
#orient = orientation of data. Default is columns (keys of dict = columns), if keys should be rows, pass index.

#np.strings.count(a,sub[,start,end]
#Returns array with the number of non-overlapping occurrences of substring sub in the range [start, end].


# The cumulative counts:
# how many times in Chapter 1, how many times in Chapters 1 and 2, and so on.
cum_counts = counts.cumsum()
#.cumsum() is a pandas method that adds the values for each row with the values from the previous row,
# returning a dataframe with the cumulative sum for each row.
print(cum_counts)

# Add the chapter numbers
number_of_chapters = len(book_chapters) #No of chapters = length of book chapters list
cum_counts['Chapter'] = np.arange(number_of_chapters)
#Cumulative count for each chapter = range 0 - whatever the final chap number is
#np.arange(start (optional):end (default is end of array) ) creates an array of evenly spaced values within an interval.

# Do the plot
cum_counts.plot(x='Chapter')
plt.title('Cumulative Number of Times Each Name Appears');

plt.show()


#---------------ACQUIRING INFO THAT IS TEDIOUS TO ACQUIRE BY HAND
# In each chapter, count the number of all characters;
# Also count the number of periods.
chars_periods = pd.DataFrame.from_dict({
        'Number of chars in chapter': [len(s) for s in book_chapters], #length for each item in book chapters
        'Number of periods': np.char.count(book_chapters, '.') #count of '.' in book chapters
    })
print(chars_periods)

plt.figure(figsize=(6, 6))
plt.scatter(chars_periods['Number of periods'],
            chars_periods['Number of chars in chapter'],
            color='darkblue')

plt.show()