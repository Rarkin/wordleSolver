# variables for player guess, set to canoe my favorite starting word 
guess = ""
# variable for result w = wrong letter g = correct letter & place y = correct letter wrong place
result = '"'

# get word list from txt file
word_list_file = open("possibleWords.txt", "r")

possible_words = word_list_file.read().split()

word_list_file.close()

# find the wrong letters in a guess
def incorrectLetters(result, guess):
    wrong_letters = []
    for i in range(0, 5):
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
    for i in range(0, 5):
        if result[i] == "g":
            correct_letters.append([guess[i], i])
    return correct_letters

def letterFrequency(possible_words):
    """
    For each letter in the alphabet, count the number of times it appears in each position of the word
    
    :param possible_words: a list of all possible words that can be made from the letters in the hand
    :return: A dictionary with the key being the letter and the value being a list of the frequency of
    that letter in each position.
    """
    alhpabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet_dict = {}
    for char in alhpabet:
        freq = [0,0,0,0,0]
        for i in range(0, 5):
            for word in possible_words:
                if word[i] == char:
                    freq[i] += 1
            alphabet_dict.update({char: freq})
    return alphabet_dict

def score(possible_words, frequencies):
    """
    It takes a list of possible words and a dictionary of frequencies and returns a dictionary of words
    and their scores
    
    :param possible_words: a list of all possible words that can be made from the letters in the rack
    :param frequencies: a dictionary of dictionaries. The keys are the letters of the alphabet, and the
    values are dictionaries of the form {0: frequency, 1: frequency, 2: frequency, 3: frequency, 4:
    frequency}
    :return: A dictionary of words and their scores.
    """
    word_dict = {}
    max_frequency = [0,0,0,0,0]
    for char in frequencies:
        for i in range(0, 5):
            if max_frequency[i] < frequencies[char][i]:
                max_frequency[i] = frequencies[char][i]
    for word in possible_words:
        word_score = 1
        for i in range(0,5):
            char = word[i]
            word_score *= 1 + (frequencies[char][i] - max_frequency[i]) ** 2
        word_dict.update({word: word_score})
    return word_dict

def bestPossibleWord(possible_words, frequencies):
    """
    For each word in the list of possible words, calculate the score of that word, and if that score is
    less than the current best score, update the best score and the best word
    
    :param possible_words: a list of words that are possible to be the best word
    :param frequencies: a dictionary of letter frequencies, where the keys are letters and the values
    are the frequencies of those letters
    :return: The best word is being returned.
    """
    max_score = 999999999
    best_word = "canoe"
    word_score = score(possible_words, frequencies)
    for word in possible_words:
        if word_score[word] < max_score:
            max_score = word_score[word]
            best_word = word
    return best_word


def incorrectWordRemover(result, guess, possible_words):
    """
    It removes words from the list of possible words that contain letters that are not in the result,
    letters that are in the result but in the wrong place, and letters that are in the result but in the
    wrong place and are also in the wrong place in the guess
    
    :param result: the result of the guess
    :param guess: the word that the user guessed
    :param possible_words: list of all possible words
    :return: A list of words that are still possible to be the secret word.
    """
    wrong_letters = incorrectLetters(result, guess)
    correct_but_wrong = correctButWrongPlace(result, guess)
    correct_letters = correctLetterCorrectPlace(result, guess)
    
    good_letters = []
    for correctLetter in correct_letters:
        good_letters.append(correctLetter[0])
    for correctButWrong in correct_but_wrong:
        good_letters.append(correctButWrong[0])
    
# This is the first step in removing words from the list of possible words. It removes words that
# contain letters that are not in the result.
    potential_words_one = []
    for word in possible_words:
        check = 0
        for wrongLetter in wrong_letters:
            if wrongLetter in word:
                if wrongLetter in good_letters:
                    pass
                else:
                    check = 1                
        if check == 0:
            potential_words_one.append(word)

# This is the second step in removing words from the list of possible words. It removes words that
# contain letters that are in the result but in the wrong place.
    potential_words_two = []
    for word in potential_words_one:
        check = 0 
        for correctLetter in correct_letters:
            if word[correctLetter[1]] != correctLetter[0]:
                check = 1
                break
        if check == 0:
            potential_words_two.append(word)

# This is the third step in removing words from the list of possible words. It removes words that
# contain letters that are in the result but in the wrong place.
    potential_words_three = []
    for word in potential_words_two:
        check = 0 
        for correctButWrong in correct_but_wrong:
            if word[correctButWrong[1]] == correctButWrong[0]:
                check = 1
                break
        if check == 0:
            potential_words_three.append(word)
    
# This is the fourth step in removing words from the list of possible words. It removes words that
# contain letters that are not in the list of good letters.
    potential_words_four = []
    for word in potential_words_three:
        check = 0
        for correctLetter in good_letters:
            if correctLetter not in word:
                check = 1
                break
        if check == 0:
            potential_words_four.append(word)

# This is the fifth step in removing words from the list of possible words. It removes words that
# contain letters that are in the list of good letters but not the correct number of times.
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
    guess = input().lower()
    print("Enter your first result: remember w = wrong letter | g = correct letter in correct place | y = correct letter in incorrect place")
    result = input().lower()
    counter = 1
    while result != "ggggg" and counter < 6:
        possible_words = incorrectWordRemover(result, guess, possible_words)
        print(possible_words)
        if len(possible_words) == 0:
            break
        wordSuggestion = bestPossibleWord(possible_words, letterFrequency(possible_words))
        print("i suggest you try: ", wordSuggestion)
        print("Enter you next guess: ")
        guess = input().lower()
        print("Enter your result,  remember w = wrong letter | g = correct letter in correct place | y = correct letter in incorrect place")
        result = input().lower()
        counter += 1
    if len(possible_words) == 0:
        print("hmmm looks like you made a mistake")
    elif counter == 6 and result != "ggggg":
        print("to many guesses better luck next time")
    else:
        print("Looks like we won :)")

solveWordle(possible_words)