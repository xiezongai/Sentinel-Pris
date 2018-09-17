# -*- coding:utf-8 -*-
import re
import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import warnings

warnings.filterwarnings('ignore')


class Tfidf(object):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def del_punctuation(self, string):
        string = re.sub(u'[,，。.!！?？、《》#~@$^&*()（）<>/-—【】～~\'‘’“”{}…]', '', string)
        string = re.sub('\s{2,}', ' ', string)
        return string

    def cosine_similarity_tfidf(self, corpus, cand_query_list):
        # vectorizer = TfidfVectorizer()
        result_dict = {}
        vectors = self.vectorizer.fit_transform(corpus).toarray()
        # print self.vectorizer.get_feature_names()
        # print vectors
        for i in range(len(cand_query_list)):
            cosine_similarity = np.dot(vectors[-1], vectors[i]) / (
                        np.linalg.norm(vectors[-1]) * np.linalg.norm(vectors[i]))
            norm_sim = 0.5 + 0.5 * cosine_similarity
            result_dict[cand_query_list[i]] = norm_sim
        return result_dict

    def main(self, user_query, cand_query_list, value):
        user_query = ' '.join(jieba.cut(self.del_punctuation(user_query)))
        cand_query_lists = [' '.join(jieba.cut(self.del_punctuation(each))) for each in cand_query_list]
        cand_query_lists.append(user_query)
        corpus = cand_query_lists
        time_start = time.time()
        result_dict = self.cosine_similarity_tfidf(corpus, cand_query_list)
        time_end = time.time()
        # print(time_start - time_end, "s")
        result_tup = sorted(result_dict.items(), key=lambda item: item[1], reverse=True)
        result = result_tup[0]
        if result[-1] > value:
            # print(result[0],result[1])
            # return result_dict
            return result
        else:
            return None


if __name__ == "__main__":
    test = Tfidf()
    sentence1 = '日本好玩吗'
    sentence2 = ["日本神户有什么好玩的",
                 "日本的ギャルゲーム有什么好玩的",
                 "日本白滨有什么好玩的",
                 "日本有什么>好玩的地方想去玩",
                 "日本有什么好玩的小玩意吗",
                 "日本有什么好玩的，好看的我好想去日本啊，可是不知道玩什么",
                 "日本有什么好玩的地方",
                 "日本东京好玩>吗，有什么好玩的地方日本东京好玩吗，有什么好玩的地方只有去过的说",
                 "日本仙台有什么好玩的么",
                 "日本东京好玩吗，有什么好玩的地方",
                 "日本神户有什么好吃的好玩的",
                 "日本秋季有什么好玩的我准备去日本玩，不知道秋季日本有什么好玩的，",
                 "日本名古屋有什么好玩的地方如题有什么好玩的地方，环境怎么样>有什么特色",
                 "日本有什么好玩的"]
    # for k, v  in test.main(sentence1,sentence2).items():
    # print (k,v)
    a = test.main(sentence1, sentence2, 0.1)
    print(a)
