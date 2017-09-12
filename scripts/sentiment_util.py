import nltk as nt
import constants
import re

from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn


def filter_sentiment_words(data, stopwords, senti_words):
    """
    Input: single document (string)
    return string contain sentiment word separated with space
    """

    if isinstance(data, list) or isinstance(data, tuple):
        raise TypeError('Must be string')

    collect = []

    for sentence in nt.sent_tokenize(data):
        for word_tag in nt.pos_tag(nt.word_tokenize(sentence)):
            word, tag = word_tag
            if tag in constants.POS_LIST.keys() and (word not in stopwords):
                if word in senti_words:
                    collect.append(stemming(word))
                else:
                    sen_sets = wn.synsets(word, pos=constants.POS_LIST.get(tag))
                    if sen_sets:
                        a = swn.senti_synset(sen_sets[0].name())
                        if a:
                            if a.obj_score() <= 0.7:
                                collect.append(stemming(word))
    return ' '.join(list(set(collect)))


def get_lemma_text(text):
    '''
    Return space separated lemmas, excluding spaces, urls, #s, emails, stop words, and proper nouns
    '''
    return ' '.join([t.lemma_.lower() for t in text if (t.is_punct==False) &
                                                (t.is_space==False) &
                                                (t.like_url==False) &
                                                (t.like_num==False) &
                                                (t.like_email==False) &
                                                (t.is_stop==False) &
                                                (t.pos_!='PROPN')])


def get_sentimental_word():
    # return set of sentiment words

    words = []
    for word in open('sentiment_words.txt'):
        words.append(word.strip())
    return set(words)


def get_stop_words():
    # return set of stopwords
    stopwords = []
    for word in open('stopwords.txt'):
        stopwords.append(word.strip())
    return set(stopwords)


def lower_and_replace(data, stopwords, senti_words):
    """
    Input: list or tuple of document or it may be single document
    return sentiment word (list of list or list)
    """

    temp = []
    if isinstance(data, list) or isinstance(data, tuple):
        for doc in data:
            temp.append(replace_words(doc.lower(), stopwords, senti_words))
        return temp

    elif isinstance(data, str):
        return [replace_words(data.lower(), stopwords, senti_words)]

    else:
        raise TypeError('Must be a list, tuple or string')


def replace_words(data, stopwords, senti_words):

    """
    Input: single document (string)
    return string
    """

    for means, pattern in constants.REGEX.iteritems():
        data = re.sub(pattern, " " + means + " ", data)
    data = re.sub('[\.\+\?%_"]+', " ", data)
    return filter_sentiment_words(data, stopwords, senti_words)


def stemming(word):
    """
    Input: single word
    return stemmed word
    """

    try:
        word = nt.PorterStemmer().stem(word)
    except:
        pass
    return word
