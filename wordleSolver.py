# variables for player guess, set to canoe my favorite starting word 
from typing import Counter


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
def incorrectLetters(result, guess):
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

# way to give a word a score to evaluate how likely it is the correct word for the day by evaluating the letter frequencies
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

#  find the best possible word, Lower score is better, start with stupidly high score
def bestPossibleWord(possible_words, frequencies):
    max_score = 999999999
    best_word = "canoe"
    word_score = score(possible_words, frequencies)
    for word in possible_words:
        if word_score[word] < max_score:
            max_score = word_score[word]
            best_word = word
    return best_word

# remove words that cannot be correct
def incorrectWordRemover(result, guess, possible_words):
    wrong_letters = incorrectLetters(result, guess)
    correct_but_wrong = correctButWrongPlace(result, guess)
    correct_letters = correctLetterCorrectPlace(result, guess)
    good_letters = []
    for correctLetter in correct_letters:
        good_letters.append(correctLetter[0])
    for correctButWrong in correct_but_wrong:
        good_letters.append(correctButWrong[0])
    
    potential_words_one = []
    for word in possible_words:
        check = 0
        for wrongLetter in wrong_letters:
            if wrongLetter in word:
                if wrongLetter in good_letters:
                    pass
                else:
                    check = 1
                    break
        if check == 0:
            potential_words_one.append(word)

    potential_words_two = []
    for word in potential_words_one:
        check = 0 
        for correctLetter in correct_letters:
            if word[correctLetter[1]] != correctLetter[0]:
                check = 1
                break
        if check == 0:
            potential_words_two.append(word)
    
    potential_words_three = []
    for word in potential_words_two:
        check = 0 
        for correctButWrong in correct_but_wrong:
            if word[correctButWrong[1]] == correctButWrong[0]:
                check = 1
                break
        if check == 0:
            potential_words_three.append(word)
    
    potential_words_four = []
    for word in potential_words_three:
        check = 0
        for correctLetter in good_letters:
            if correctLetter not in word:
                check = 1
                break
        if check == 0:
            potential_words_four.append(word)
    
    potential_words_five = []
    for word in potential_words_four:
        check = 0
        for wrongLetter in wrong_letters:
            if wrongLetter in good_letters:
                if word.count(wrongLetter) != good_letters.count(wrongLetter):
                    check = 1
                    break
        if check == 0:
            potential_words_five.append(word)
    
    return potential_words_five

# Game solver logic and loop
def solveWordle(possible_words):
    print("Time to solve a wordle with the help of magic :)")
    print("w = wrong letter | g = correct letter in correct place | y = correct letter in incorrect place")
    print("i like to start with the word canoe so why not give that a try")
    print("Enter your first guess:")
    guess = input()
    print("Enter your first result: remember w = wrong letter | g = correct letter in correct place | y = correct letter in incorrect place")
    result = input()
    counter = 1
    while result != "ggggg" and counter < 6:
        possible_words = incorrectWordRemover(result, guess, possible_words)
        print(possible_words)
        if len(possible_words) == 0:
            break
        wordSuggestion = bestPossibleWord(possible_words, letterFrequency(possible_words))
        print("i suggest you try: ", wordSuggestion)
        print("Enter you next guess: ")
        guess = input()
        print("Enter your result,  remember w = wrong letter | g = correct letter in correct place | y = correct letter in incorrect place")
        result = input()
        counter += 1
    if len(possible_words) == 0:
        print("hmmm looks like you made a mistake")
    elif counter == 6 and result != "ggggg":
        print("to many guesses better luck next time")
    else:
        print("Looks like we won :)")

solveWordle(possible_words)