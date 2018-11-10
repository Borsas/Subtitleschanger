#! /usr/bin/python
# -*- encoding : utf-8 -*-
import os
import fileinput
import subprocess
from collections import OrderedDict


# Rip the .ass subtitles file from the .mkv using ffmpeg
def subs(file):
    file_ass = file.replace('.mkv', '.ass')
    subprocess.call(['ffmpeg', '-i', file, '-map', '0:s:0', file_ass])
    replace(file_ass)


# Got from https://www.daniweb.com/programming/software-development/code/216636/multiple-word-replace-in-text-python
def multiplereplace(text, worddict):
    for key in worddict:
        text = text.replace(key, worddict[key])
    return text


# Generates \\N to dictionary keys and values
def dictionaryadd(olddict):
    new_list = {}
    for item in olddict:
        key = item.split(" ")
        value = olddict[item].split(" ")
        # Add newline to the front of the second word
        if len(key) == 2 and len(value) == 2:
            new_key = key[0] + " \\N" + key[1]
            new_value = value[0] + " \\N" + value[1]
            new_list[new_key] = new_value
        # Add newline to the front of the first word
        else:
            new_key = "\\N" + key[0]
            new_value = "\\N" + value[0]
            new_list[new_key] = new_value
    # Combines the original and new dictionaries
    new_list.update(olddict)
    return new_list


# Change the keywords in the subtitle file
def replace(ass):
    # Key is the old name, value is the new name
    subtitles = {
        'Golden Wind': 'Gold Experience',
        'Reverb': 'Echoes',
        'Shadow Sabbath': 'Black Sabbath',
        'Zipper Man': 'Sticky Fingers'
    }
    file_ass = os.path.join(os.getcwd(), ass)

    lista = dictionaryadd(subtitles)

    with fileinput.FileInput(file_ass, inplace=True) as file:
            for line in file:
                print(multiplereplace(line, lista))


def main():
    print('Subs replacer')
    episodes = {}

    # Just for testing
    os.chdir('L:/Anime/JoJo/JoJo part 5/')

    # Get all .mkv files in the folder and number them
    for ep in os.listdir(os.getcwd()):
        if ep.endswith('.mkv'):
            num = ep.split()[8]
            if num.startswith('0'):
                num.split('0')
                episodes[num[1]] = ep
            else:
                episodes[num] = ep

    episodes = OrderedDict(sorted(episodes.items()))
    for i in episodes:
        print(i, "-", episodes[i])
    file = input('Select the file: ')
    subs(episodes[file])


if __name__ == '__main__':
    main()