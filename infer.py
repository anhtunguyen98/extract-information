from config import *
from pyvi import ViPosTagger,ViTokenizer
from joblib import load
class ModelInfer:
    def __init__(self):
        self.crf=load(MODEL_DIR)

    def is_number(self,s):
        try:
            complex(s)  # for int, long, float and complex
        except ValueError:
            return False

        return True

    def word2features(self,sent, pos, i):
        word = sent[i]
        features = {
            'bias': 1.0,
            'word': word,
            'word.is_number()': self.is_number(word),
            'word.isalpha()': word.isalpha(),
            'pos': pos[i]
        }
        if i > 1:
            word2 = sent[i - 2]
            features.update({
                '-2:word': word2,
                '-2:word.is_number()': self.is_number(word2),
                '-2:word.isalpha()': word2.isalpha(),
                '-2:pos': pos[i - 2],
            })
        elif i > 0:
            word1 = sent[i - 1]
            features.update({
                '-1:word': word1,
                '-1:word.is_number()': self.is_number(word1),
                '-1:word.isalpha()': word1.isalpha(),
                '-1:pos': pos[i - 1],
            })
        else:
            features['BOS'] = True

        if i < len(sent) - 2:
            word2 = sent[i + 2]
            features.update({
                '+2:word': word2,
                '+2:word.is_number()': self.is_number(word2),
                '+2:word.isalpha()': word2.isalpha(),
                '+2:pos': pos[i + 2],
            })

        elif i < len(sent) - 1:
            word1 = sent[i + 1]
            features.update({
                '+1:word': word1,
                '+1:word.is_number()': self.is_number(word1),
                '+1:word.isalpha()': word1.isalpha(),
                '+1:pos': pos[i + 1],
            })
        else:
            features['EOS'] = True
        return features

    def sent2features(self,sent, pos):
        return [self.word2features(sent, pos, i) for i in range(len(sent))]

    def process(self,sentence, poss):
        new_sentence, new_pos = [], []
        for word, pos in zip(sentence, poss):
            tokenized_word = word.split("_")
            n_word = len(tokenized_word)
            new_sentence.extend(tokenized_word)
            new_pos.extend([pos] * n_word)
        return new_sentence, new_pos
    def res_sentence(self,test_sentence):
        test_sentence=ViTokenizer.tokenize(test_sentence)
        test_sentence, pos = ViPosTagger.postagging(test_sentence)
        new_words, pos = self.process(test_sentence, pos)
        X_test=self.sent2features(new_words,pos)
        new_tags=self.crf.predict_single(X_test)
        st1, st2 = [], []
        for i in range(len(new_words)):
            if new_tags[i] == 'O':
                if new_tags[i - 1] != 'O':
                    st1.append(new_words[i])
                    st2.append('O')
                    print(i)
                    continue
                else:
                    if i==0:
                        st1.append(new_words[i])
                        st2.append('O')
                    else:
                        st1[-1] = st1[-1] + '_' + new_words[i]
            elif new_tags[i][0] == 'B':
                tag = "" + new_tags[i][2:]

                st1.append(new_words[i])
                st2.append(tag.upper())

            elif new_tags[i][0] == 'I':
                st1[-1] = st1[-1] + '_' + new_words[i]
        return st1, st2


