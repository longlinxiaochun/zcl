class lexicon(object):

    def __init__(self):
        self.vocabulary = {
            'north': 'direction',
            'south': 'direction,',
            'east': 'direction',
            'go': 'verb',
            'kill': 'verb',
            'eat': 'verb',
            'the': 'stop',
            'in': 'stop',
            'of':'stop',
            'bear':'noun',
            'princess': 'noun',
            '3': 'number',
            '91234': 'number',
            '1234': 'number',
            'ASDFADFASDF': 'error',
            'IAS': 'error'
        }
        self.list = []

    def scan(self, stuff):
        self.list = []
        self.stuff = stuff
        self.words = self.stuff.split()

        for word in self.words:
            if word.isdigit():
                self.list.append(self.vocabulary[word], int(word))
            else:
                self.list.append(self.vocabulary[word], word)
        return self.list

lexicon = lexicon()