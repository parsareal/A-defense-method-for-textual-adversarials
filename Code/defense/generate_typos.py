import string

class GenerateTypos:
    def __init__(self, vocab):
        self.vocab = vocab
        self.alphabet_list = list(string.ascii_lowercase)
        
    # Swap
    def return_swaps(self, string):
        swaps = [] 
        for i in range(len(string) - 1):
            tmp = list(string)
            tmp[i] = string[i+1]
            tmp[i+1] = string[i]
            tmp = ''.join(tmp)
            if tmp in self.vocab:
                swaps.append(tmp)
        return swaps

    #Insertion
    def return_insertions(self, string):
        insertions = []
        for i in range(len(string) + 1):
            for c in self.alphabet_list:
                tmp = list(string)
                tmp.insert(i, c)
                tmp = ''.join(tmp)
                if tmp in self.vocab:
                    insertions.append(tmp)
        return insertions

    #Deletion
    def return_deletions(self, string):
        deletions = []
        for i in range(len(string)):
            tmp = list(string)
            del tmp[i]
            tmp = ''.join(tmp)
            if tmp in self.vocab:
                deletions.append(tmp)
        return deletions

    #Replace
    def return_replaces(self, string):
        replaces = []
        for i in range(len(string)):
            for c in self.alphabet_list:
                tmp = list(string)
                tmp[i] = c
                tmp = ''.join(tmp)
                if tmp in self.vocab:
                    replaces.append(tmp)
        return replaces

    def get_all_possibles_of_words(self, string):
        string = string.lower()
        cands = self.return_swaps(string) + self.return_insertions(string) + self.return_deletions(string) + self.return_replaces(string)
        cands = list(dict.fromkeys(cands))
        if string in cands:   
            cands.remove(string)
        return cands
