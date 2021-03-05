import nltk
import copy
import spacy
# nltk.download('punkt')

class Preprocess:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def split_to_sents(self, text):
        # sents = nltk.sent_tokenize(text)
        doc = self.nlp(text)
        return [sent.text for sent in doc.sents]

    def adv_tokenizer(self, sentence):
        # tokens = nltk.word_tokenize(sentence)
        doc = self.nlp(sentence)
        return [token.text for token in doc]

    def generate_masks(self, tokens):
        masked_sents = []
        for i in range(len(tokens)):
            tmp = tokens[i]
            tokens[i] = "[MASK]"
            # tmp_toks = copy.deepcopy(tokens)
            masked_sents.append(" ".join(tokens))
            tokens[i] = tmp
        return masked_sents

# str_input = "I didn't not is the firts month of year. I am going to bust. Hi!"
# input_tokens = adv_tokenizer(str_input)
# generate_masks(input_tokens)
# split_to_sents(str_input)