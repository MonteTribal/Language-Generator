#-------------------------------------------------------------------------------
# Name:        Language Generator
# Purpose: This is a small program that makes up words, based on other words
#
# Author:      Eric Monteforte - aka: MonteTribal
#   MonteforteEric@gmail.com
#   Eric@lanternlightstudios.com
#
# Created:     12/01/2017 (Thats January 12, 2017 to be specific)
# Copyright:   (c) Eric 2017
# Licence:     nice try internet, my driver's licence # is my own!
#
# Created with Python 3.1.2 (r312:79149, Mar 21 2010, 00:41:52)
# I believe that i have nothing special going into this as
# I believe re, os, and random are all stock installs with python
#
# Contains: main.py - the entire program
#           Seed.txt - the seed file. contains real words to generate new ones
#
# I am sure this idea isn't completely unique. Props to all the
# linguists who actually know what they are doing. I am bad word user.
#-------------------------------------------------------------------------------

import re
import os
from random import randint
from random import sample

NUM_WORDS = 100 #this is not a hard set number of words, merely a suggestion
FILE_NAME = ""

###
### WORD CREATION PIECES
###
#how words may start with consonants
ConsonantsWordsMayStartWith = set()
#how words may start with vowels
VowelsWordsMayStartWith = set()
#consonants filling the words
wordFillersConsonants = set()
#vowels fillings the words
wordFillersVowels = set()
#how words may end
wordEndersConsonants = set()
wordEndersVowels = set()
#how many sections a word may have
wordPieceLength = set()
#number of seed words
seedCount = 0
#number of words starting with Vowels vs Consonants
wordsStartWithConsonants = 0
wordsStartWithVowels = 0

def ReadSeed():

    #ah yes, Python global things. I break all sorts of rules because FUCK IT
    global ConsonantsWordsMayStartWith
    global VowelsWordsMayStartWith
    global wordFillersConsonants
    global wordFillersVowels
    global wordEndersConsonants
    global wordEndersVowels
    global wordPieceLength
    global seedCount
    global wordsStartWithConsonants
    global wordsStartWithVowels

    seed = open('seed.txt', 'r')
    for line in seed:
        seedCount += 1
        line = line.lower()
        if(line[0] not in 'aeiouAEIOU'): #word starts with a consonant
            wordsStartWithConsonants+=1
            r = re.findall("([^aeiou]+)([aeiou]*)", line)
            bits = []
            for pair in r:
                if (pair[0].strip() != ''): bits.append( pair[0].strip() )
                if (pair[1].strip() != ''): bits.append( pair[1].strip() )
            #print(bits)
            wordPieceLength.add(len(bits))
            for i in range(len(bits)):
                temp = bits[i]
                #word starters
                if(i == 0):
                    ConsonantsWordsMayStartWith.add(bits[0])
                #word enders
                elif(i == len(bits)-1):
                    if bits[i][0].lower() not in 'aeiou': #consonants
                        wordEndersConsonants.add(bits[i])
                    else:
                        wordEndersVowels.add(bits[i])
                #word filler
                else:
                    if bits[i][0].lower() not in 'aeiou': #consonants
                        wordFillersConsonants.add(bits[i])
                    else:
                        wordFillersVowels.add(bits[i])
        else:
            wordsStartWithVowels+=1
            r = re.findall("([aeiou]+)([^aeiou]+)", line)
            bits = []
            for pair in r:
                if (pair[0].strip() != ''): bits.append( pair[0].strip() )
                if (pair[1].strip() != ''): bits.append( pair[1].strip() )
            #print(bits)
            wordPieceLength.add(len(bits))
            for i in range(len(bits)):
                #word starters
                if(i == 0):
                    VowelsWordsMayStartWith.add(bits[0])
                #word enders
                elif(i == len(bits)-1):
                    if bits[i][0].lower() not in 'aeiou': #consonants
                        wordEndersConsonants.add(bits[i])
                    else:
                        wordEndersVowels.add(bits[i])
                #word filler
                else:
                    if bits[i][0].lower() not in 'aeiou': #consonants
                        wordFillersConsonants.add(bits[i])
                    else:
                        wordFillersVowels.add(bits[i])
    seed.close()

def PrintWordPieces():
    print("ConsonantsWordsMayStartWith " + str(ConsonantsWordsMayStartWith))
    print("VowelsWordsMayStartWith " + str(VowelsWordsMayStartWith))
    print("wordFillersConsonants " + str(wordFillersConsonants))
    print("wordFillersVowels " + str(wordFillersVowels))
    print("wordEndersConsonants " + str(wordEndersConsonants))
    print("wordEndersVowels " + str(wordEndersVowels))
    print("wordPieceLength " + str(wordPieceLength))
    print("seedCount " + str(seedCount))
    print("wordsStartWithConsonants " + str(wordsStartWithConsonants))
    print("wordsStartWithVowels " + str(wordsStartWithVowels))

def GenerateWords(wordCount):

    newWords = set()

    vowelStartingWords = wordsStartWithVowels/seedCount
    vowelStartingWords = int(wordCount) * vowelStartingWords
    vowelStartingWords = int(vowelStartingWords)
    consonantStartingWords = wordCount - vowelStartingWords
    #WORDS BEGINNGING WITH CONSONANTS
    for x in range(consonantStartingWords):
        word = ""
        word += sample(ConsonantsWordsMayStartWith, 1)[0]
        rangeLen = sample(wordPieceLength,1)[0]
        for y in range(1, rangeLen):
            if(y == rangeLen-1 and y%2 == 0):
                if(len(wordEndersConsonants) > 0):
                    word += sample(wordEndersConsonants, 1)[0]
            elif(y == rangeLen-1 and y%2 == 1):
                if(len(wordEndersVowels) > 0):
                    word += sample(wordEndersVowels, 1)[0]
            elif(y%2 == 1):
                word += sample(wordFillersVowels, 1)[0]
            elif(y%2 == 0):
                word += sample(wordFillersConsonants, 1)[0]
        if(len(word) > 1):
            newWords.add(word)
    #WORDS BEGINNING WIH VOWELS
    for x in range(vowelStartingWords):
        word = ""
        word += sample(VowelsWordsMayStartWith, 1)[0]
        rangeLen = sample(wordPieceLength,1)[0]
        for y in range(1, rangeLen):
            if(y == rangeLen-1 and y%2 == 0):
                if(len(wordEndersVowels) > 0):
                    word += sample(wordEndersVowels, 1)[0]
            elif(y == rangeLen-1 and y%2 == 1):
                if(len(wordEndersConsonants) > 0):
                    word += sample(wordEndersConsonants, 1)[0]
            elif(y%2 == 1):
                word += sample(wordFillersConsonants, 1)[0]
            elif(y%2 == 0):
                word += sample(wordFillersVowels, 1)[0]
        if(len(word) > 1):
            newWords.add(word)
    return newWords

def PrintSetOfWords(words):
    words= sorted(words)
    print( "\n".join(str(w) for w in words) )

def SaveWordsToFile(words, file_name):
    words= sorted(words)
    x =  "\n".join(str(w) for w in words)

    filename = ""
    if file_name is not "":
        filename = "GeneratedLanguages\\"+file_name+".txt"
    else:
        filename = "GeneratedLanguages\\"+sample(words, 1)[0]+".txt"

    if not os.path.exists("GeneratedLanguages\\"):
        os.makedirs("GeneratedLanguages\\")

    f = open(filename , 'w')
    f.write(x)

    f.write("\n\nWORDS USED TO SEED THIS FILE\n")
    seed = open('seed.txt', 'r')
    for line in seed:
        f.write(line)
    seed.close()

    f.close()
    print(filename + " generated")

def main():
    ReadSeed()
    PrintWordPieces()
    words = GenerateWords(NUM_WORDS)
    #PrintSetOfWords(words)
    SaveWordsToFile(words, FILE_NAME)


if __name__ == '__main__':
    main()
