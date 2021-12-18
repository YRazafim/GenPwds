#!/usr/bin/python3

import sys, itertools

#################
### VARIABLES ###
#################

# Custom words to work with
CUSTOM_WORDS = ["admin", "azerty"]

# Wordlist path to work with
WORDLIST = None

# Mix words or not
# MAX_MIXED_LENGTH = Max length of combinations (Must be >= 2)
MIXED_WORDS = True
MAX_MIXED_LENGTH = 2
SEPARATORS = ["-", "_"]

# Case modification or not
CASE_MODIF = True

# L33t or not
LEET = True
LEET_MAP = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 'z': '2'}

# Years with 4/2 digits
YEARS4 = True
YEARS2 = True
Y4 = [str (x) for x in range (2020, 2021)]
Y2 = [str (x) for x in range (12, 14)]

# Special characters or not
SPECIAL_CHARS = True
SCHARS = ["!", "*", "#", "&", "@", "$"]

#############
### MAIN ####
#############

def mix_words_length (words, length):
    new_list = []
    for permutation in itertools.permutations (words, length):
        for separator in SEPARATORS:
            output = []
            for c in itertools.product (' ' + separator, repeat = len (permutation) - 1):
                output.append (('%s'.join (permutation) % c).replace (' ', ''))
            new_list += output
    return new_list

def mix_words (words):
    new_list = []
    for i in range (2, MAX_MIXED_LENGTH+1):
        new_list += mix_words_length (words, i)
    return new_list

def modif_case (words):
    new_list = []
    for word in words:
        new_list += list (map (''.join, itertools.product (*zip (word.upper(), word.lower()))))
    return new_list

def leet_word (word):
    possibles = []
    for l in word:
        ll = LEET_MAP.get (l.lower(), l.lower())
        possibles.append ((l,) if ll == l.lower() else (l, ll))
    return [''.join(t) for t in itertools.product (*possibles)]

def leet (words):
    new_list = []
    for word in words:
        new_list += leet_word (word)
    return new_list

if __name__ == "__main__":
    if (len (sys.argv) != 2):
        print ("\n[ERROR] Usage : {} <OutputFileName>\n".format (sys.argv[0]))
        exit()

    print ("\n[+] Generating wordlist ...")

    # Add custom words
    DIC = CUSTOM_WORDS

    # Add words in wordlist
    if (WORDLIST != None):
        with open (WORDLIST, "r") as wd:
            words = wd.readlines()
            for word in words:
                DIC += [word.replace ("\n", "")]

    # Mix words up to MAX_MIXED_LENGTH combinations
    l = len (DIC)
    if (l > 1 and MIXED_WORDS and MAX_MIXED_LENGTH > 1):
            if (MAX_MIXED_LENGTH > l):
                print ("[ERROR] MAX_MIXED_LENGTH must be <= len (DIC)\n")
                exit()
            else:
                DIC = mix_words (DIC)

    # Apply case modifications
    DIC = modif_case (DIC)

    # Apply l33t
    if (LEET):
        DIC = leet (DIC)

    # Add years and special chars
    new_list = []
    for word in DIC:
        new_list += [word]
        if (YEARS4):
            for y4 in Y4:
                tmp = word + y4
                new_list += [tmp]
                if (SPECIAL_CHARS):
                    for schar in SCHARS:
                        new_list += [tmp + schar]
        if (YEARS2):
            for y2 in Y2:
                tmp = word + y2
                new_list += [tmp]
                if (SPECIAL_CHARS):
                    for schar in SCHARS:
                        new_list += [tmp + schar]
        if (not YEARS4 and not YEARS2 and SPECIAL_CHARS):
                for schar in SCHARS:
                    new_list += [word + schar]
    DIC = new_list

    with open (sys.argv[1], "w+") as ofile:
        for word in DIC:
            ofile.write (word + "\n")

    print ("[OK] Done\n")
