from collections import defaultdict

class WordIndex:

    def __init__(self, min_count = 0):
        self.word_counts = defaultdict(int)
        self.min_count = min_count
        #RNN's pad with zero
        for word in ['PAD', 'BOS', 'EOS']:
            self.word_counts[word] = 1
        
    def fillCounts(self, dialogue):
        for word in dialogue:
            self.word_counts[word] += 1
            
    def getIndicies(self):
        return {word:index for index, word in enumerate(self.word_counts) if self.word_counts[word] > self.min_count}
