# coding: utf-8
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

with open('data.csv', 'r') as f:
    data = f.readlines()
texts, sentences = [], []
for i in range(1, len(data)):
    final = []
    text = data[i].split('\t')[5]
    dialogs = text.split('\\n')
    for d in dialogs:
        fi = d.split('\\t')[-1]
        final.append(fi)
    sentences.append(final)

class data():
    def __init__(self):
        self.texts = list(pd.read_csv('cut_result.csv')['cut_result'])

    def get_bag_of_words(self):
        corpus = self.texts
        vectorizer = CountVectorizer()
        vectorizer.fit(corpus)
        return vectorizer, vectorizer.transform(corpus)

    def get_tfidf_dict(self):
        dic = {}
        vectorizer, X = self.get_bag_of_words()
        tfidf_transformer = TfidfTransformer()
        tfidf_transformer.fit(X.toarray())
        for idx, word in enumerate(vectorizer.get_feature_names()):
            dic[word.encode('utf-8')] = tfidf_transformer.idf_[idx]
        tfidf = tfidf_transformer.transform(X)
        return dic, tfidf

data_util = data()
dic, tfidf = data_util.get_tfidf_dict()

class compose():
    def __init__(self, dic, tfidf_bottom_limit, tfidf_top_limit, sentences):
        self.dic = dic
        self.bottom_limit = tfidf_bottom_limit
        self.top_limit = tfidf_top_limit
        self.sentences = sentences

    def get_new_stopwords(self):
        stopwords = []
        for key in self.dic:
            if dic[key] < self.bottom_limit or dic[key] > self.top_limit:
                stopwords.append(key)
        return stopwords

    # 对句子进行分词
    def seg_sentence(self, sentence):
        sentence_seged = jieba.cut(sentence.strip())
        stopwords = self.get_new_stopwords()
        stopwords = [x.decode() for x in stopwords]
        leftlist = ['信用卡', '账单', '申请', '额度', '消费', '短信', '卡片', '还款', '申请'
            , '办理', '银行', '金额', '交易', '密码', '分期', '查询', '登记', '手机', '服务'
            , '取消', '本期', '信息', '卡号', '使用', '提前', '查询', '登记', '手机', '服务'
            , '账户', '刷卡', '业务', '我查', '中信', '手续费', '还清', '欠款', '号码', '手机号码'
            , '设置', '记录', '中信银行', '调整', '自动', '收取', '资料', '开通', '积分', '利息'
            , '交卡', '交过', '白金卡', '支付', '提供', '激活', '本人', '身份证', '咨询', '后期', '费用', '本金', '方式', '年费', '语音', '具体', '查看'
            , '先不换', '储蓄银行', '储值卡', '借款人', '保密', '保障卡', '价位', '付通', '付给', '付清']
        deletelist = ['就', '您', '我', '没', '啊', '嗯', '那']
        stopwords = list(set(stopwords + deletelist) - set(leftlist))
        outstr = ''
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += ""
        return outstr

    def get_new_text(self):
        new_text = []
        for i in range(len(self.sentences)):
            print(i / len(self.sentences))
            sentence = self.sentences[i]
            new_sentence = []
            sent_num = len(sentence)
            for j in range(sent_num):
                cut_res = self.seg_sentence(sentence[j])
                new_sentence.append(''.join(cut_res))
            new_text.append(new_sentence)
        return new_text