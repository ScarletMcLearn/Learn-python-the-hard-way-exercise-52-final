class ParserError(Exception):
    pass

# This is the final result 
class Sentence(object):
    def __init__(self,subject,verb,obj):
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = obj[1]

# returns the type of the first word, always happens
def peek(word_list):
    if word_list:
        word=word_list[0]
        return word[0]
    else:
        return None

# pops a value
def match(word_list,expecting): #given expecting == noun
    if word_list: #if word list has sth
        word = word_list.pop(0)  #pop first element which is a tuple from lexicon

        if word[0] == expecting: #if noun  == noun(if type in tuple (type,word) is noun)
            return word
        else:
            return None
    else:
        return None


# Match method isn't meant to return
def skip(word_list,word_type):
    while peek(word_list) == word_type:
        match(word_list,word_type)


def parse_verb(word_list):
    # skip pops a value without saving that value
    skip(word_list,'stop')

    if peek(word_list) == 'verb':
        return match(word_list,'verb')
    else:
        raise ParserError("Expected a verb next. ")



def parse_object(word_list):
    # skip pops a value without saving that value
    skip(word_list,'stop')
    next_word = peek(word_list)

    if next_word == 'noun':
        return match(word_list,'noun')
    elif next_word == 'direction':
        return match(word_list,'direction')
    else:
        raise ParserError("Expected a noun or direction next.")

def parse_subject(word_list):
    # skip pops a value without saving that value
    skip(word_list, 'stop')
    next_word = peek(word_list)

    if next_word == 'noun':
        return match(word_list,'noun')
    elif next_word =='verb':
        return ('noun','player')
    else:
        raise ParserError("Expected a verb next.")

def parse_sentence(word_list):
    subj = parse_subject(word_list)
    verb = parse_verb(word_list)
    obj = parse_object(word_list)

    return Sentence(subj,verb,obj)

