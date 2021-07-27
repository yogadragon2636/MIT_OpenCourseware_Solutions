# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from pset4a_soln import iterations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = str(text)
        self.valid_words = load_words(WORDLIST_FILENAME)


    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        transpose_dict_upper = dict()
        transpose_dict_lower = dict()
        
        vowels_list_perm = list(vowels_permutation)
        vowels_list_lower = list(VOWELS_LOWER)
        vowels_list_upper = list (VOWELS_UPPER)
        for i in range(0,5):
            transpose_dict_lower[vowels_list_lower[i]] = vowels_list_perm[i]
            transpose_dict_upper[vowels_list_upper[i]] = vowels_list_perm[i].upper()
        transpose_dict_combine = {**transpose_dict_lower,**transpose_dict_upper}
        return transpose_dict_combine
#        vowels_perm_list = vowels_permutation.split('')
#        print (vowels_perm_list)
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        message_list = list(self.message_text)
        for i in range(0, len(message_list)):
            if message_list[i] in transpose_dict:
                message_list[i] = transpose_dict[message_list[i]]
        return ''.join(message_list)

def invert_dict(d):
    return {v: k for k, v in d.items()}

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        vowel_iterations = iterations(VOWELS_LOWER)
        message_letter_list = list(self.message_text)
        message_letter_list_copy = message_letter_list.copy()
        valid_word_count_total = 0
        best_shifted_string = self.message_text
#        print (vowel_iterations)
        for i in range(0, len(vowel_iterations)):
            valid_word_count_this_permutation = 0
            encrypt_dict = self.build_transpose_dict(vowel_iterations[i])
            decrypt_dict = invert_dict(encrypt_dict)
#            print ('Encrypt Dict: ', encrypt_dict, '   Decrypt Dict: ', decrypt_dict)
            for j in range(0,len(message_letter_list)):
                if message_letter_list[j] in decrypt_dict:
                    message_letter_list_copy[j] = decrypt_dict[message_letter_list[j]]
#                    print ('I changed a ',message_letter_list[j], 'to a ', message_letter_list_copy[j])
                    
            decrypted_string = ''.join(message_letter_list_copy)
            print (decrypted_string)
            word_list = decrypted_string.split()
            for k in word_list:
                word = k.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
                print (word)
                if word.lower() in self.valid_words:
                    valid_word_count_this_permutation = valid_word_count_this_permutation+1
            if valid_word_count_this_permutation > valid_word_count_total:
                valid_word_count_total = valid_word_count_this_permutation
                current_best_shift = vowel_iterations[i]
                best_shifted_string = decrypted_string
#                print('Curent Shift: ', vowel_iterations[i], '     Shifted String: ', best_shifted_string, 'Current Best Shift: ', current_best_shift, '     Valid Word Count Total: ', valid_word_count_total)
        return (best_shifted_string)
#message = EncryptedSubMessage('This is my test message')
message = EncryptedSubMessage('aeilfkgj ejbiklabne ieldjgnblel')


#print(message.decrypt_message())

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
#    TODO: WRITE YOUR TEST CASES HERE
