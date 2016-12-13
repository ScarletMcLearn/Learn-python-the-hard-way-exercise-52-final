#lexicon
lexicon ={
        'north':'direction',
        'south':'direction',
        'east':'direction',
        'west':'direction',
        'bear':'noun',
        'princess':'noun',
        'go':'verb',
        'kill':'verb',
        'eat':'verb',
        'the':'stop',
        'in':'stop',
        'of':'stop',
        'tell':'verb',
        'joke':'noun',
        'place':'verb',
        'bomb':'noun',
        'shoot!':'verb',
        'dodge!':'verb',
        'throw':'verb',
        'a':'stop',
        'slowly':'stop',
        'gothon':'noun',
        'shot':'noun',


        }

def scan(sentence):
    words = sentence.lower().split()
    result = []
    for word in words:
        try:
            pair=(lexicon[word],word)
        except KeyError:
            try:
                pair=('number',int(word))
            except ValueError:
                pair=('error',word)
        result.append(pair)

    return result





