#! /usr/bin/python
# -*- encoding : utf-8 -*-
import os
import fileinput
import subprocess
import sys
import time


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


# Change the keywords in the ass subtitle file
def replace(ass):
    # Key is the old name, value is the new name
    subtitles = {}

    with open('subs.txt', 'r') as file:
        for sub in file:
            word = sub.split(':')
            if '\n' in word[1]:
                word[1] = word[1][:-1]
            subtitles[word[0]] = word[1]
    file_ass = os.path.join(os.getcwd(), ass)

    lista = dictionaryadd(subtitles)

    with fileinput.FileInput(file_ass, inplace=True) as file:
            for line in file:
                print(multiplereplace(line, lista))


def main():
    # Checks if the subtitle file actually exists
    if not os.path.isfile('subs.txt'):
        print('Could not find "subs.txt", exiting')
        time.sleep(3)
        sys.exit()

    # Get all .mkv files in the folder
    for ep in os.listdir(os.getcwd()):
        # Checks if the file is .mkv
        if ep.endswith('.mkv'):
            ep_ass = ep[:-4] + '.ass'
            if not os.path.isfile(ep_ass):
                subs(ep)


if __name__ == '__main__':
    main()
