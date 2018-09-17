from sklearn import svm
import jieba
import numpy as np
import gensim
import pickle as pkl
from scipy.spatial.distance import pdist


wordvec_size = 300
zero_pad = [0 for n in range(wordvec_size)]
vec_model = gensim.models.Word2Vec.load('../model/word2vec.model')
print("成功导入词向量")

def get_vec(sentence):
    s = jieba.cut(sentence)
    count = 0
    sum = zero_pad

    for eachword in s:
        try:
            temp = vec_model[eachword]
            count = count + 1
        except KeyError:
            temp = zero_pad
        sum = np.array(sum) + np.array(temp)
    x = {}
    if count == 0:
        x[0] = sentence
        x[1] = zero_pad
        return x
    else:
        x[0] = sentence
        x[1] = sum / count
        return x


def predict(model, sentence):
    """
    @param sentence : str
    """
    vec = get_vec(sentence)[1]
    return svm_model.predict_proba([vec])[0][1]   # 正样本的概率

def getsimlist_vec(list):
    """
    匹配库向量化
    :param list: ["", ""]
    :return: [("", np.array([]))]
    """
    result = []
    for eachsentence in list:
        wordlist = jieba.cut(eachsentence)
        count = 0
        sum = zero_pad
        for eachword in wordlist:
            try:
                temp = vec_model[eachword]
                count = count + 1
            except KeyError:
                temp = zero_pad
            sum = np.array(sum) + np.array(temp)
        if count == 0:
            continue
        x = {}
        x[0] = eachsentence
        x[1] = sum / count
        result.append(x)
    return result

def getscore(sentence_vec, sim_vec):
    """
    计算两个向量的余弦相似度
    :param sentence_vec: np.array([]))
    :param sim_vec: np.array([]))
    :return: score
    """
    if list(sentence_vec) == list(zero_pad):
        score = 1
    else:
        score = pdist(np.vstack([sentence_vec, sim_vec]), 'cosine')
    return 1 - score

def word2vec_sim(sentence_vec, simlist_vec, threshold=0.5):
    """
    :param sentence_vec: 单个句子的向量
    :param simlist_vec: 匹配库向量list
    :param threshold: 0.5
    :return: [score, source, matched_sentence]
    """
    sim_temp_list = []
    sim_temp = float(threshold)
    for eachsim in simlist_vec:
        score = getscore(sentence_vec[1], eachsim[1])
        if score > sim_temp:
            sim_temp = score
            sim_temp_list = [sim_temp, sentence_vec[0], eachsim[0]]
        else:
            continue
    if not sim_temp_list:
        return None
    else:
        return sim_temp_list

def get_sim_from_txt(path):
    with open(path, 'r', encoding="utf-8") as f:
        return f.readlines()

# path = 'app/analyzers/smart_text_analyzer/把握需求.txt'
# simlist = get_sim_from_txt(path)
# simlist_vec = getsimlist_vec(simlist)

# s = '您看您是不是办理这个业务'
# res = word2vec_sim(get_vec(s), simlist_vec, 0.5)

if __name__ == '__main__':
    with open("model/把握需求", 'rb') as f:
        svm_model = pkl.load(f)
    print(predict(svm_model, "你好"))
