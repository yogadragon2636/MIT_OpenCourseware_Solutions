# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = str(text)
        self.valid_words = load_words('words.txt')

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return str(self.message_text)

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        letter_dict_lower = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',10:'k',11:'l',12:'m',13:'n',14:'o',15:'p',16:'q',17:'r', 18:'s',19:'t',20:'u',21:'v',22:'w',23:'x',24:'y', 25:'z'}
        letter_dict_upper = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R', 18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y', 25:'Z'}
        letter_dict_shift_lower={}
        letter_dict_shift_upper = {}
        for i in letter_dict_lower:
            new_key = (i + shift)%26 
            letter_dict_shift_lower[letter_dict_lower[i]] = letter_dict_lower[new_key]
        for i in letter_dict_upper:
            new_key = (i + shift)%26 
            letter_dict_shift_upper[letter_dict_upper[i]] = letter_dict_upper[new_key]
        combine_shift_dic = letter_dict_shift_lower.copy()
        combine_shift_dic.update(letter_dict_shift_upper)
        return combine_shift_dic

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        special_chars_string = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""
        shift_dict = self.build_shift_dict(shift)
        input_message = str(self)
        encoded_message=''
        for i in input_message:
            if i in special_chars_string:
                encoded_message = encoded_message + i
            else: 
                encoded_message = encoded_message + shift_dict[i]
        return encoded_message
        
    def __str__(self):
        return self.message_text
    

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
#Use Message init method to initialize valid_words and message_text
        Message.__init__(self, text)
#Initialize shift, encryption dict, encrypted message
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)


    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict_copy = self.encryption_dict.copy()
        return encryption_dict_copy

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.apply_shift(self.shift)

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)



#print (plaintext)
#print (plaintext.get_shift())
#print (plaintext.get_encryption_dict())
#print (plaintext.get_message_text_encrypted())
#
#plaintext.change_shift(7)
#
#print (plaintext.get_shift())
#print (plaintext.get_encryption_dict())
#print (plaintext.get_message_text_encrypted())


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        valid_word_count_total = 0
        current_best_shift = 0
        best_shifted_string =''
        for i in range(-25,-0):
            valid_word_count_this_shift = 0
#            shift_dict = self.build_shift_dict(i)
            shifted_word = self.apply_shift(i)
            word_list = shifted_word.split()
#            print (word_list)
            for k in word_list:
                if k in self.valid_words:
                    valid_word_count_this_shift = valid_word_count_this_shift + +1
            if valid_word_count_this_shift > valid_word_count_total:
                valid_word_count_total = valid_word_count_this_shift
                current_best_shift = abs(i)
                best_shifted_string = shifted_word
            print('Curent Shift: ', i, '     Shifted String: ', best_shifted_string, 'Current Best Shift: ', current_best_shift, '     Valid Word Count Total: ', valid_word_count_total)
        return (current_best_shift, best_shifted_string)
plaintext = PlaintextMessage('This is a test message', -3)        
#print (plaintext)
#print (plaintext.get_shift())
#print (plaintext.get_encryption_dict())
#print (plaintext.get_message_text_encrypted())

plaintext.change_shift(9)

#print (plaintext.get_shift())
#print (plaintext.get_encryption_dict())
#print (plaintext.get_message_text_encrypted())

ciphertext = CiphertextMessage(plaintext.get_message_text_encrypted())

print ('CipherText is: ', ciphertext)
print(ciphertext.decrypt_message())

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story 
    
    pass #delete this line and replace with your code here
