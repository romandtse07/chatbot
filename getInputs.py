from collections import defaultdict

class WordIndex:

    def __init__(self, min_count = 0):
        self.word_counts = defaultdict(int)
        self.min_count = min_count
        
    def fillCounts(self, dialogue):
        for word in dialogue:
            self.word_counts[word] += 1
            
    def getIndicies(self):
        return {word:index for index, word in enumerate(self.word_counts) if self.word_counts[word] > self.min_count}
