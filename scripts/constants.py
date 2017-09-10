REGEX = {
    "happy": ":\-?[\)\]D]",
    "sad": ":'?\-?\(",
    'shock': ":\-O|:\-\(\)",
    "uneasy": ":\-/",
    "evil": ">:\-[\(D]",
    " ": "(http[s]?:\/\/)?([\w_-]+(?:(?:\.[\w_-]+)+))" +
         "([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
}


# turney POS list
SENTI_POS = ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG',
             'VBN', 'VBP', 'VBZ']

# ,'NN', 'NNS', 'NNP', 'NNPS'
FIRST_LIST = ["JJ", "RB", "RBR", "RBS", "NN", "NNS"]
SECOND_LIST = ["JJ", "NN", "NNS", "VB", "VBD", "VBN", "VBG"]
THIRD_LIST = ["NN", "NNS"]

# ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
POS_LIST = {
    'VB': 'v',
    'VBD': 'v',
    'VBG': 'v',
    'VBN': 'v',
    'VBP': 'v',
    'VBZ': 'v',
    'JJ': 'a',
    'JJR': 'a',
    'JJS': 'a',
    'RB': 'r',
    'RBR': 'r',
    'RBS': 'r',
    'NN': 'n',
    'NNS': 'n',
    'NNPS': 'n',
}
