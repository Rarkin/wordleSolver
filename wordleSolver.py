# variables for player guess, set to canoe my favorite starting word 
guess = "canoe"
# variable for result w = wrong letter g = correct letter & place y = correct letter wrong place
result = '"wgyww'

# get word list from txt file
word_list_file = open("possibleWords.txt", "r")

possible_words = []
for line in word_list_file:
    possible_words = [(line.split()) for line in word_list_file]

word_list_file.close()

# find the wrong letters in a guess
def wrongLetter(result, guess):
    wrong_letters = []
    for i in range(0,5):
        if result[i] == "w":
            wrong_letters.append(guess[i])
        return wrong_letters

# find letters that are correct but in the wrong place in the guess
def correctButWrongPlace(result, guess):
    correct_but_wrong = []
    for i in range(0,5):
        if result[i] == "y":
            correct_but_wrong.append([guess[i], i])
        return correct_but_wrong

# find letters that are correct & in the correct place in the guess
def correctLetterCorrectPlace(result, guess):
    correct_letters = []
    for i in range(0,5):
        if result[i] == "g":
            correct_letters.append([guess[i], i])
        return correct_letters

# create a dictionary to that holds each letter of the alphabet and map to 5 positions
# then find freq of the letter in each position this will be used when evaluating how likely a word is to be correct
def letterFrequency(possible_words):
    alhpabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet_dict = {}
    for char in alhpabet:
        frequency = [0,0,0,0,0]
        for i in range(0,5):
            for word in possible_words:
                if word[i] == char:
                    frequency[i] += 1
            alphabet_dict.update({char: frequency})
    return alphabet_dict

# way to give a word a score to evaluate how likely it is the correct word for the day
# 
def score(possible_words, frequencies):
    word_dict = {}
    max_frequency = [0,0,0,0,0]
    for char in frequencies:
        for i in range(0,5):
            if max_frequency[i] < frequencies[char][i]:
                max_frequency[i] = frequencies[char][i]
    for word in possible_words:
        word_score = 1
        for i in range(0,5):
            char = word[i]
            word_score *= 1 + (frequencies[char][i] - max_frequency[i]) ** 2
        word_dict.update({word: word_score})
    return word_dict