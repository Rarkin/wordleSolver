# variables for guess & result 
guess = "canoe"
# w = wrong g = correct letter & place y = correct letter wrong place
result = '"wgyww'

# find the wrong letters in a guess
def wrongLetter(result, guess):
    wrong_letters = []
    for i in range(0,5):
        if result[i] == "w":
            wrong_letters.append(guess[i])
        return wrong_letters

