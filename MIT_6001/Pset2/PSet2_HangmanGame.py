import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    wordlength=len(secret_word)
    lengthtest=0
    for i in secret_word:
        for j in letters_guessed:
            if i==j:
                lengthtest += 1
                break
    return lengthtest == wordlength

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
        lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
        assumes that all letters are lowercase
    returns: string, letters guessed with _'s representing unguessed letters
    '''
    word=[]
    for i in secret_word:
        for j in letters_guessed:
            if i==j:
                word.append(i)
                spacetest = False
                break
            spacetest= True
        if spacetest == True:
            word.append('_ ')
    wordstring = ''.join(word)
    return wordstring

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far;
        assumes that all letters are lowercase
    returns: string containing unguessed letters
    '''
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    for i in letters_guessed:
        alphabet.remove(i)
            
    wordstring = ''.join(alphabet)
    return wordstring

def match_with_gaps(my_word, other_words):
    my_word= my_word.replace('_ ','_')
    my_word_list = list(my_word)
    letters_guessed = set(my_word)
    other_words_list=list(other_words)
    if len(my_word)!=len(other_words):
        return False
    else:
        for i in range(len(my_word)-1):
            if my_word_list[i] == '_':
#                print ('There is a _ here')
                for j in letters_guessed:
#                    print ('iterating on j')
#                    print (j, other_words_list[i])
                    if j == other_words_list[i]:
                        return False
#                        print('break')
                        break
            elif my_word_list[i]==other_words_list[i]:
                word_match = True
            else:
                word_match = False
                break
        return word_match

    
    
def show_possible_matches(my_word):
    for i in wordlist:
        DoesWordMatch=match_with_gaps(my_word, i)
        if DoesWordMatch == True:
            print (i)
            
def hangman(secret_word):
    num_guesses = 6
    num_warnings=3
    print('Welcome to the game of hangman!')
    print('I am thinking of a word that is ', len(secret_word), ' letters long!')
    print('You have ', num_warnings, 'warnings left')
    print('--------------------')
    print('You have ', num_guesses, 'guesses left') 
    

    letters_guessed=[]
    game_over = is_word_guessed(secret_word, letters_guessed)
    while game_over==False:
        print('Available Letters:', get_available_letters(letters_guessed))
        current_letter_guess=input('Please guess a letter.')
        current_letter_guess=str.lower(current_letter_guess)
        isletteralpha = str.isalpha(current_letter_guess)
        if current_letter_guess == '*':
            isletterast = True
        else:
            isletterast=False
        print('Letters Guessed:', letters_guessed)
        is_letter_in_word = False
        isletterguessed = False
        for i in letters_guessed:
            if i == current_letter_guess:
                isletterguessed = True
        if isletterast == True:
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            num_guesses = num_guesses -1
            print ('You now have ', num_guesses, 'guesses left')
        elif isletteralpha == True and isletterguessed == False:
            letters_guessed.append(current_letter_guess)
            for i in secret_word:
                if i == current_letter_guess:
                    print(current_letter_guess, ' is in the secret word! You have', num_guesses, ' guesses left')
                    is_letter_in_word = True
                    break
            if is_letter_in_word==False:
                for i in ['a', 'e','i','o','u']:
                    if i == current_letter_guess:
                        num_guesses = num_guesses -1

                num_guesses=num_guesses - 1
                print(current_letter_guess, ' is NOT the secret word! You have', num_guesses, ' guesses left')                    
            print(get_guessed_word(secret_word, letters_guessed))
            print('----------')
        else:
            if num_warnings>0:
                num_warnings = num_warnings - 1
                print('Oops! Please enter a letter you have not guessed! You have ', num_warnings, ' warnings left before you lose a guess')
            else:
                num_guesses -= 1
                print('Oops! Please enter a letter you have not guessed!  You have no warnings left. You lose one guess and have ', num_guesses, 'remaining')
        game_won = is_word_guessed(secret_word, letters_guessed)
        game_over = is_word_guessed(secret_word, letters_guessed) or num_guesses == 0
    if game_won==True:
        print ('Congratulations, you won!')
        print ('Your total score this game is:', len(''.join(set(secret_word))) * num_guesses)
    else:
        print ('Sorry, you ran out of guesses.  The word was ', secret_word, '.')
hangman_word= choose_word(wordlist)
#hangman_word = 'apple'
hangman_output= hangman(hangman_word)








