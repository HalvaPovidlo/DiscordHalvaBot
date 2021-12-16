from string import punctuation
import Levenshtein as lev


def preprocess_text(text):
    tokens = text.lower().split(" ")

    tokens = [token for token in tokens if token != " " and token.strip() not in punctuation]
    text = " ".join(tokens)
    return text


def compute_df(word, corpus):
    return sum([1.0 for i in corpus if word in i]) / len(corpus)


class Searcher:
    def __init__(self, titles):
        self.corpus = titles
        self.corpus_prp = [preprocess_text(doc).split(",")[0].split(" ") for doc in self.corpus]
        self.uniq_words_corpus = set([_ for i in range(len(self.corpus_prp)) for _ in self.corpus_prp[i]])

    def _get_closest_levenstein_word(self, token, top_k=10):
        top_token = [" " for _ in range(top_k)]
        top_score = [0.0 for _ in range(top_k)]

        for t in self.uniq_words_corpus:
            temp_score_lev = lev.ratio(token, t)
            for i in range(top_k):
                if temp_score_lev > top_score[i]:
                    old_t = top_token[i]
                    old_score = top_score[i]

                    for j in range(i + 1, top_k):
                        temp_score = top_score[j]
                        temp_token = top_token[j]

                        top_score[j] = old_score
                        top_token[j] = old_t

                        old_score = temp_score
                        old_t = temp_token

                    top_score[i] = temp_score_lev
                    top_token[i] = t
                    break

        return [top_token, top_score]

    def get_prediction(self, word, a=0.9):
        top_k_words, top_k_scores = self._get_closest_levenstein_word(word, top_k=20)
        d = {}
        for t, sc in zip(top_k_words, top_k_scores):
            new_score = compute_df(t, self.corpus_prp) * a + sc * (1 - a)
            d.update({t: new_score})

        return sorted(d.items(), key=lambda item: item[1], reverse=True)
