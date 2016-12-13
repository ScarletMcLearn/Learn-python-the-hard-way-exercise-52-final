from nose.tools import *
from bin import lexicon_parser
word = [('noun','princess'),('verb','kill')]

def test_peek():
    word = [('noun','princess'),('verb','kill')]
    assert_equal(lexicon_parser.peek(word),'noun')

def test_match():
    word = [('noun','princess'),('verb','kill')]
    assert_equal(lexicon_parser.match(word ,'noun'),('noun','princess'))
    assert_equal(lexicon_parser.match([],'noun'),None)
    assert_equal(lexicon_parser.match(["eaver"],'verb'),None)

def test_skip():
    newword = [('noun','princess'),("noun","spider"),('verb','kill')]
    lexicon_parser.skip(newword,'noun')
    assert_equal(newword, [('verb','kill')])



def test_parse_object():
    newword = [('noun','princess'),("noun","spider"),('verb','kill')]
    newword1 = [('stop','this'),('noun','princess'),("noun","spider"),('verb','kill')]
    newword2 = [('stop','this'),('direction','north'),("noun","spider"),('verb','kill')]
    assert_raises(lexicon_parser.ParserError , lexicon_parser.parse_object,[('verb,','fight'),('stop','this'),('verb','nigga')])
    assert_equal(lexicon_parser.parse_object(newword),('noun','princess'))
    assert_equal(lexicon_parser.parse_object(newword1),('noun','princess'))
    assert_equal(lexicon_parser.parse_object(newword2),('direction','north'))



def test_parse_verb():
    word = [('noun','princess'),("noun","spider"),('verb','kill')]
    word1 = [('stop','ok'),('stop','this'),('verb','kill')]
    assert_raises(lexicon_parser.ParserError,lexicon_parser.parse_verb,word)
    assert_equal(lexicon_parser.parse_verb(word1),('verb','kill'))


def test_pass_subject():
    word = [('direction','north'),("noun","spider"),('verb','kill')]
    word1 = [('stop','ok'),('stop','this'),('verb','kill')]
    assert_raises(lexicon_parser.ParserError,lexicon_parser.parse_subject,word)
    assert_equal(lexicon_parser.parse_subject([('noun','princess'),('verb','kill')]),('noun','princess'))
    assert_equal(lexicon_parser.parse_subject([('verb','kill')]),('noun','player'))



def test_parse_sentence():
    word = [('noun','princess'),('verb','kills'),('noun','bear')]
    word1 = [('direction','north'),('noun','princess'),('noun','bear')]
    sentence = lexicon_parser.parse_sentence(word)
    assert_equal(sentence.subject,'princess')
    assert_equal(sentence.verb,'kills')
    assert_equal(sentence.object,'bear')
    word2 =  [('noun','princess'),('verb','goes'),('direction','north')]
    sentence2 = lexicon_parser.parse_sentence(word2)
    assert_equal(sentence2.subject,'princess')
    assert_equal(sentence2.verb,'goes')
    assert_equal(sentence2.object,'north')
    assert_raises(lexicon_parser.ParserError,lexicon_parser.parse_sentence,word1)



