# Created by Helic on 2018/7/29
import uuid
import os
import pickle as pkl
import gensim
from .utils import *
# from .tfidfTestSklearn import Tfidf
from .VsmTest import levenshteinStr, levenshteinList
from .ml_classify import *


MAX_RESULT = 10


class SmartTextAnalyzer:
    def __init__(self, analyzer_id, matched_sentences, prob, target, analyzer_type, keywords):
        self.analyzer_id = analyzer_id
        self.matched_sentences = matched_sentences  # list
        self.prob = prob  # 分类器的threshold
        self.target = target
        self.name = analyzer_type
        self.keywords = keywords  # list
        if self.name in ["辱骂指责"]:
            self.model = None  # 辱骂指责没有分类器，只有关键词
        else:
            self.load_classify_model()
        if self.name in ["用心超越期望", "换位思考"]:
            self.embedding_matched_sentences = getsimlist_vec(self.matched_sentences)

    @classmethod
    def load(cls, analyzer_id, matched_sentences, prob, target, name, keywords):
        """
        返回一个SmartTextAnalyzer instance
        """
        return cls(analyzer_id, matched_sentences, prob, target, name, keywords)

    def load_classify_model(self, model_path="app/analyzers/smart_text_analyzer/model"):
        """
        读取model.pkl文件，初始化一个svm分类模型
        @param model_path : "app/analyzers/smart_text_analyzer/model" 注意需要加上self.name才是最终的路径
        """
        model_path = os.path.join(model_path, self.name)
        with open(model_path, 'rb') as f:
            self.model = pkl.load(f)
            print("成功导入 TextAnalyzer_{} 机器学习分类模型".format(self.name))

    def test(self, dialogs):
        '''
        TODO: Batch Load Dialogs to save time 测试多个对话
        @param dialogs : [{"transcripts": [{},{}], "id": str}, {"transcripts": [{},{}], "id": str}]
        '''
        matched = []
        for dialog in dialogs:
            result = self.run(transcripts = dialog["transcripts"], dialog_id = dialog["id"])
            if len(result['matched']):
                matched.append({
                    "dialog_id": dialog['id'],
                    "matched": result["matched"],
                    "transcripts" : str(dialog["transcripts"]),
                    "target": self.target
                })
            if len(matched) == MAX_RESULT:
                return matched
        return matched

    def run(self, transcripts, dialog_id):
        """
        @Description: 针对于单个text analyzer做测试,只测试一个对话
        @param  transcripts [{"speech": <string>, "target": <string>, "start_time": <string>, "end_time": <string>}]
        @return {
                "dialog_id": "1000",
                "matched": [
                    {
                        "score": 0.5454545454545454,
                        "source": "没有了",
                        "matched": "那我也没有办法了",
                        "start_time": "08:06:38",
                        "end_time": "08:06:43",
                        "origin": "没有了没有了"
                    }
                ]
            }
        """
        total_matched=[]
        for sentence in transcripts:
            content = sentence['speech']
            start_time = sentence['start_time']
            end_time = sentence['end_time']
            target = sentence["target"]
            if self.name in ["辱骂指责"]:   # 对于辱骂指责，只使用关键词检测
                if self.keywords_test(sentence=content)['status']:
                        total_matched.append({
                            "score": "1",
                            "source": content,
                            "matched": self.keywords_test(sentence=content)['matched'],
                            "start_time": start_time,
                            "end_time": end_time,
                            "origin": content
                        })
            elif self.name in ["用心超越期望", "换位思考"]:
                if self.target == "客户" and target == "客户":
                    if self.embedding_test(sentence=content, prob=self.prob):
                        score, source, matched_sentence = self.embedding_test(sentence=content, prob=self.prob)
                        total_matched.append({
                                "score": str(score),
                                "source": content,
                                "matched": matched_sentence,
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
            else:
                if self.target == "all":
                    if len(content) < 10:
                        if self.keywords_test(sentence=content)['status']:
                            total_matched.append({
                                "score": "1",
                                "source": content,
                                "matched": self.keywords_test(sentence=content)['matched'],
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
                    else:  # 句子长度大于10
                        matched = self.ml_test(sentence=content)
                        if matched > self.prob:
                            total_matched.append({
                                "score": str(matched),
                                "source": content,
                                "matched": "机器学习分类",
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
                elif self.target == "坐席" and target == "坐席":
                    if len(content) < 10:
                        if self.keywords_test(sentence=content)['status']:
                            total_matched.append({
                                "score": "1",
                                "source": content,
                                "matched": self.keywords_test(sentence=content)['matched'],
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
                    else:  # 句子长度大于10
                        matched = self.ml_test(sentence=content)
                        if matched > self.prob:
                            total_matched.append({
                                "score": str(matched),
                                "source": content,
                                "matched": "机器学习分类",
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
                elif self.target == "客户" and target == "客户":
                    if len(content) < 10:
                        if self.keywords_test(sentence=content)['status']:
                            total_matched.append({
                                "score": "1",
                                "source": content,
                                "matched": self.keywords_test(sentence=content)['matched'],
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
                    else:  # 句子长度大于10
                        matched = self.ml_test(sentence=content)
                        if matched > self.prob:
                            total_matched.append({
                                "score": str(matched),
                                "source": content,
                                "matched": "机器学习分类",
                                "start_time": start_time,
                                "end_time": end_time,
                                "origin": content
                            })
        if len(total_matched) != 0:
            return{"dialog_id": dialog_id, "matched": total_matched, "target": "all"}
        return {"dialog_id": dialog_id, "matched": []}

    def keywords_test(self, sentence):
        """
        检测对话句子里是否包含关键词
        :param sentence: str
        :return: {"status": bool, "matched": ""}
        """
        for word in self.keywords:
            if word in sentence:
                return {"status": True, "matched": word}
        return {"status": False, "matched": ""}

    def ml_test(self, sentence):
        """
        使用分类器检测一个句子是否属于某个类别
        @param sentence : str
        @return prob : float 正样本的概率
        """
        vec = get_vec(sentence)[1]
        return self.model.predict_proba([vec])[0][1]   # 正样本的概率

    def embedding_test(self, sentence, prob):
        return word2vec_sim(get_vec(sentence), self.embedding_matched_sentences, prob)