from transformers import BertTokenizer, BertForMaskedLM, TFBertForMaskedLM
import tensorflow as tf
import torch
import numpy as np

class MainDefense:
    def __init__(self, generateTypos, preprocess):
        self.generateTypos = generateTypos
        self.preprocess = preprocess
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForMaskedLM.from_pretrained('bert-base-uncased')
        # self.model = TFBertForMaskedLM.from_pretrained('bert-base-cased')

    # str_input = "the best form of the tea is [MASK] from a plant."
    # str_input = "the best form of the tea is liberalism by this plant."
    # str_input = "Handshaking is a veery bad kind of salutation."
    # str_input = "[MASK] is the firts month of year."
    # str_input = "I didn't d is the firts month of year."

    def calculate_score(self, str_input):
        inputs = self.tokenizer(str_input, return_tensors="pt", padding = True)
        input_ids = inputs["input_ids"][0].detach().numpy()
        # input_ids = inputs["input_ids"][0].numpy()
        mask_index = np.where(input_ids == 103)[0]
        if len(mask_index) > 0:
            mask_index = mask_index[0]

        outputs = self.model(**inputs)
        logits = outputs[0]

        log_prob = 0
        for i in range(1, len(input_ids) - 1):
            token_logits = logits[0][i].detach().numpy()
            # token_logits = logits[0][i].numpy()
            sum_all = np.sum(token_logits)
            if i == mask_index:
                max_index = np.argmax(token_logits)
                log_prob += np.log(np.abs(token_logits[max_index]/sum_all))
            else:
                log_prob += np.log(np.abs(token_logits[input_ids[i]]/sum_all))
            
        # print('log_prob: ' + str(log_prob))
        return log_prob
        # np.argmax(logits[0][8].detach().numpy())
        # print(logits.shape)
        # logs = logits[0][1].detach().numpy()
        # tokens = sorted(range(len(logs)), key=lambda i: logs[i])[-100:]

        # nominates = tokenizer.convert_ids_to_tokens(tokens)


    def gain_candidates(self, sentence):
        alpha = 3
        tokens = self.preprocess.adv_tokenizer(sentence)
        masked_sentences = self.preprocess.generate_masks(tokens)

        probs = []
        for masked_sent in masked_sentences:
            probs.append(self.calculate_score(masked_sent))
        # print(np.mean(probs))
        tmp_indice = sorted(range(len(probs)), key=lambda i: probs[i])[-2:]
        candidate_indice = []
        for cindice in tmp_indice:
            if np.abs(probs[cindice] - np.mean(probs)) > alpha:
                candidate_indice.append(cindice)

        return candidate_indice


    # sentence = "Cable News Network is a multinational news-based paye television channel headquartered in New York City."

    def check_improvement(self, cands, index, sent_tokens, origin_sent_prob):
        # beta = 10
        good_cands = dict()
        for cand in cands:
            sent_tokens[index] = cand
            cand_score = self.calculate_score(" ".join(sent_tokens))
            if cand_score - origin_sent_prob > 0:
                good_cands[cand] = cand_score - origin_sent_prob
        return good_cands

    def check_sentence(self, sentence):
        adv_cands = self.gain_candidates(sentence)
        tokens = self.preprocess.adv_tokenizer(sentence)
        origin_sent_prob = self.calculate_score(" ".join(tokens))
        for i in adv_cands:
            adv_token = tokens[i]
            adv_token_cands = self.generateTypos.get_all_possibles_of_words(adv_token)
            good_adv_token_cands = self.check_improvement(adv_token_cands, i, tokens, origin_sent_prob)
            good_adv_token_cands = dict(sorted(good_adv_token_cands.items(), key=lambda item: item[1]))
            good_adv_tokens = list(good_adv_token_cands.keys())
            if good_adv_tokens:
                print(adv_token + ' => ' + good_adv_tokens[-1])
                tokens[i] = good_adv_tokens[-1] 
        return " ".join(tokens)


    # inp_text = 'This pllayer is playing in the feild. Whaat do yuo do in there?'
    def check_input(self, input):
        sents = self.preprocess.split_to_sents(input)
        new_input = ''
        for sent in sents:
            new_input = new_input + ' ' + self.check_sentence(sent)
        return new_input

        # check_sentence(sentence)
        # check_input(inp_text)