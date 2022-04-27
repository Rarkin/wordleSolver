# variables for guess & result 
guess = "canoe"
# w = wrong g = correct letter & place y = correct letter wrong place
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

# find that are correct & in the correct place in the guess
def correctLetterCorrectPlace(result, guess):
    correct_letter = []
    for i in range(0,5):
        if result[i] == "g":
            correct_letter.append([guess[i], i])
        return correct_letter

