from math import log10

class ngram_score(object):
    # Function to load ngrams from a file and calculate log probabilities
    def __init__(self, ngramfile, sep=' '):
        self.ngrams = {}
        with open(ngramfile) as file:  # Use context manager for handling files
            for line in file:
                key, count = line.split(sep)
                self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())  # Use values() instead of itervalues()
        # calculate log probabilities
        for key in self.ngrams:
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)

    # Function to score a text using ngrams
    def score(self, text):
        score = 0
        ngrams = self.ngrams.get
        for i in range(len(text) - self.L + 1):
            # Add the log probability of each ngram in the text
            score += ngrams(text[i:i + self.L], self.floor)
        return score
