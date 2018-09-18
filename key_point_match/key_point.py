'''
created by xuhong 2018/9/18
更改:   1.匹配库增添每个关键点的阈值
        2.完善了多种算法的选择，通过传method（string）参数选择算法，method可选'levenshtein' or 'word2vec'
        3.完善了function的注释
'''
import json
import copy
from utils import *


class KeyPoint(object):
    def __init__(self, compare_corpus_path='data/compare_corpus_11.json'):
        self.compare_corpus = corpus(compare_corpus_path) # 加载匹配库
        self.compare_corpus_vector = copy.deepcopy(self.compare_corpus)
        for topic in self.compare_corpus_vector:
                for keypoint in self.compare_corpus_vector[topic]:
                    self.compare_corpus_vector[topic][keypoint]["compared_corpus"] = getsimlist_vec(self.compare_corpus[topic][keypoint]["compared_corpus"])
        print('******初始化完成******')

    def get_similarity(self, topic, method, sentence):
        '''
        单句与匹配库匹配,返回高于每项设定的阈值的关键点的最高相似度,有多个点的取最高的
        :param topic: string, '现金分期'
        :param method: string, 'levenshtein' or 'word2vec'
        :param sentence: string
        :return result: {'sentence': "subsentence",'keypoint':'', 'score':'', 'compared_source':'匹配库句子'}
        '''
        result = []
        multi_keypoint = []
        try:
            sim_corpus = self.compare_corpus[topic]
        except KeyError:
            print('******暂不支持该业务分类下的关键点提取！******')
            exit()
        for key in sim_corpus.keys():
            keypoint_dic = {'keypoint': key, 'score': 0, 'compared_source': ''}
            top1_score = 0
            top1_key = ''
            top1_source = ''
            sim_list = sim_corpus[key]['compared_corpus']  # [str]
            if method == 'levenshtein':
                threshold = sim_corpus[key]['threshold']['levenshtein']
                score_result = levenshteinStr(sentence, self.compare_corpus[topic][key]["compared_corpus"], threshold)
            elif method == 'word2vec':
                threshold = sim_corpus[key]['threshold']['word2vec']
                score_result = w2v_model_new(sentence, self.compare_corpus_vector[topic][key]["compared_corpus"], threshold)
            if score_result != None:
                score = score_result[0]
                if score > top1_score:
                    top1_score = score
                    top1_key = key
                    top1_compared_sentence = score_result[2]
            if top1_score != 0:
                top1_score = float('%.2f' % top1_score)
                keypoint_dic = {'keypoint': key, 'score': top1_score,
                                'compared_source': top1_compared_sentence}
                multi_keypoint.append(keypoint_dic)
        if len(multi_keypoint) > 1: # 子句匹配到多个关键点时，取相似度分值最高的
            result = top_keypoint(multi_keypoint)
            result['sentence'] = sentence
        elif len(multi_keypoint) == 1:
            result = multi_keypoint[0]
            result['sentence'] = sentence
        else:
            result = None
        return result

    def deal_dialog(self, dialog, topic, N, step):
        '''
        处理输入的一段对话
        只取客服的句子，滑动窗口：对输入字符串按照窗口大小N以步长step取出，返回字符串数组
        :param dialog: list, [{"target": "坐席", "speech": "王先生您好有什么可以帮您", "start_time": "0.00", "end_time": "3.83"},{}]
        :param topic: string, '现金分期'
        :param N: int, 切分句子滑动窗口大小 10
        :param step: int, 滑窗步长 3
        :return subsentence: list, [{'sentence':subsentence1,'sen_num': num},{'sentence':subsentence2,'sen_num': num}...]
        :return index_sentence: dict, {num: "source sentence"}
        '''
        sentence = []
        subsentence = []
        index_sentence = {}
        if 'sen_num' not in dialog[0].keys():  # 如果给的句子没有标注句子序号，则自动标注，从0开始标号
            for i in range(len(dialog)):
                dialog[i]['sen_num'] = i
        for each_pare in dialog:
            if each_pare['target'] == '坐席':
                string = each_pare['speech']
                sen_num = each_pare["sen_num"]
                index_sentence[sen_num] = string
                if not string:
                    sentence = None
                if N > len(string):
                    sentence = string + '_' + str(sen_num)
                    subsentence.append(sentence)
                else:
                    res = []
                    point = N
                    while point <= len(string):
                        res.append(string[point - N: point])
                        point = point + step
                    for item in res:
                        subsen = {'sentence': item, 'sen_num': sen_num}
                        subsentence.append(subsen)
        return subsentence, index_sentence

    def subsenlist_simi(self, subsentence_list, topic, method='levenshtein'):
        '''
        对子句list进行相似度匹配，返回每个子句对应的关键点以及该关键点的相似度分值
        :param subsentence_list: list, [{'sentence':subsentence1,'sen_num': num},...]
        :param topic: string, '现金分期'
        :param method: string, 用到的算法，默认为levenshtein 可选'word2vec'
        :return result: list, [{'sentence': '', 'sen_num': 0, 'keypoint': '', 'score': 0.34, 'compared_source': '有什么疑问您可以随时致电我们客服热线。'}, ]
        '''
        result = []
        for subsentence in subsentence_list:
            sentence = subsentence['sentence']
            sentence_num = subsentence['sen_num']
            subsentence_result = self.get_similarity(topic, method, sentence)
            if subsentence_result != None:
                subsentence_result['sen_num'] = sentence_num
                result.append(subsentence_result)
        if result == []:
            return None
        else:
            return result

    def result_format(self, sentence_result, source_index=None):
        '''
        获取最终结果格式
        :param sentence_result: list, [{'sentence': '', 'sen_num': 0, 'keypoint': '', 'score': 0.34, 'compared_source': '有什么疑问您可以随时致电我们客服热线。'}, ]
        :source_index: dict, 句子index，用于获取子句对应的原句
        :return result: list, [{'keypoint':'关键点1','matched':[{"matched_sentence": "subsentence", "compared_sentence": "匹配库句子", "score":float, "source_sentence":str}]}]
        '''
        result = []
        keypoint_list = []
        if sentence_result == None:
            result = []
            return result
        for subsentence in sentence_result:
            keypoint = subsentence['keypoint']
            sentence_num = subsentence['sen_num']
            source_sentence = source_index[sentence_num]
            subsentence.pop('keypoint')
            subsentence.pop('sen_num')
            subsentence['source_sentence'] = source_sentence
            if keypoint not in keypoint_list:
                keypoint_list.append(keypoint)
                result.append({'keypoint': keypoint, 'matched': []})
            result[keypoint_list.index(
                keypoint)]['matched'].append(subsentence)
        if result == []:
            return None
        else:
            return result

    def run_levenshtein(self, dialog, topic):
        '''
        对某个业务分类下的单个对话，获取关键点及对应的句子
        :param  dialog: list,每一项为一个句子
                        示例：[
                                {
                                    "target": "坐席",
                                    "speech": "王先 生您好有什么可以帮您",
                                    "start_time": "0.00",
                                    "end_time": "3.83"
                                },,,,
                            ]
        :param  topic:  string，业务分类，示例：'现金分期'
        :param  method: string，该代码可选择两种算法，'levenshtein' or 'word2vec'
        :return result: list, 每一项为这段话匹配到的关键点之一，
                        格式：[
                                {'keypoint':'',
                                'matched':[{'sentence':'',  # 切割后的句子
                                            'compared_source':'',  # 匹配库中的句子
                                            'source_sentence':'',  # 对话中的原句（未切割）
                                            'score': float,
                                            "start_time": "08:06:38",
                                            "end_time": "08:06:43",
                                            },
                                            {},,,
                                        ]
                                },
                                {},
                            ]
                            keypoint：关键点名称，matched：关键点匹配到的句子，matched中每一项为匹配到的一个子句，包含的子句信息包括：sentence:匹配到的子句，source_sentence：子句所在的对话中的原句，compared_source：匹配库中的原句，score:相似度分值
            示例：
            [{'keypoint': '14.解释关键信息', 
              'matched': [ {'score': 0.76, 
                            'compared_source': '有什么疑问您可以随时致电我们客服热线。', 
                            'sentence': '王先 生您好有什么可', 
                            'source_sentence': '王先 生您好有什么可以帮您'},]
            }]
        '''
        subsentence_list, index_sentence = self.deal_dialog(
            dialog, topic, 10, 3)  # 分句 滑窗大小N=10，滑窗步长step=3
        dialog_result = self.subsenlist_simi(
            subsentence_list, topic, method="levenshtein")  # 对分句结果list获取匹配结果
        result = self.result_format(
            sentence_result=dialog_result, source_index=index_sentence)
        return result

    def run_word2vec(self, dialog, topic):
        '''
        对某个业务分类下的单个对话，获取关键点及对应的句子
        :param  dialog: list,每一项为一个句子
                        示例：[
                                {
                                    "target": "坐席",
                                    "speech": "王先 生您好有什么可以帮您",
                                    "start_time": "0.00",
                                    "end_time": "3.83"
                                },,,,
                            ]
        :param  topic:  string，业务分类，示例：'现金分期'
        :param  method: string，'word2vec'
        :return result: list, 每一项为这段话匹配到的关键点之一，
                        格式：[
                                {'keypoint':'',
                                'matched':[{'sentence':'',  # 切割后的句子
                                            'compared_source':'',  # 匹配库中的句子
                                            'source_sentence':'',  # 对话中的原句（未切割）
                                            'score': float,
                                            "start_time": "08:06:38",
                                            "end_time": "08:06:43",
                                            },
                                            {},,,
                                        ]
                                },
                                {},
                            ]
                            keypoint：关键点名称，matched：关键点匹配到的句子，matched中每一项为匹配到的一个子句，包含的子句信息包括：sentence:匹配到的子句，source_sentence：子句所在的对话中的原句，compared_source：匹配库中的原句，score:相似度分值
            示例：
            [{'keypoint': '14.解释关键信息', 
              'matched': [ {'score': 0.76, 
                            'compared_source': '有什么疑问您可以随时致电我们客服热线。', 
                            'sentence': '王先 生您好有什么可', 
                            'source_sentence': '王先 生您好有什么可以帮您'},]
            }]
        '''
        # subsentence_list, index_sentence = self.deal_dialog(
        #     dialog, topic, 10, 3)  # 分句 滑窗大小N=10，滑窗步长step=3
        # [{'sentence':subsentence1,'sen_num': num},{'sentence':subsentence2,'sen_num': num}...]
        subsentence_list = []
        index_sentence = {}  # {num: "source sentence"}
        for i, item in enumerate(dialog):
            subsentence_list.append({
                "sentence": item["speech"],
                'sen_num': i
            })
            index_sentence[i] = item["speech"]
        dialog_result = self.subsenlist_simi(
            subsentence_list, topic, method="word2vec")  # 对分句结果list获取匹配结果
        result = self.result_format(
            sentence_result=dialog_result, source_index=index_sentence)
        return result


if __name__ == '__main__':

    key_point = KeyPoint(compare_corpus_path='data/compare_corpus_11.json')
    dialog = [
        {
            "target": "坐席",
            "speech": "王先 生您好有什么可以帮您",
            "start_time": "0.00",
            "end_time": "3.83"
        },
        {
            "target": "客户",
            "speech": "你好你帮我查一下我这个信用卡这个月我明明都已经还完了怎么怎么又差了一万多回去了什么意思啊",
            "start_time": "3.83",
            "end_time": "17.86"
        },
        {
            "target": "坐席",
            "speech": "嗯完了又又什么又跑了一万一万多块钱过去",
            "start_time": "17.86",
            "end_time": "23.92"
        },
        {
            "target": "客户",
            "speech": "不是我的它它那个app怎么这个月还要还一万多",
            "start_time": "23.92",
            "end_time": "30.94"
        },
        {
            "target": "坐席",
            "speech": "呃稍等一下就是您信用卡本期账单还款还需要再还一万一一送一还了一万元了",
            "start_time": "30.94",
            "end_time": "41.79"
        },
        {
            "target": "客户",
            "speech": "我总共这个额度我还三万八是吗",
            "start_time": "41.79",
            "end_time": "46.25"
        },
        {
            "target": "坐席",
            "speech": "请王先生具体记录吧把您信用卡的密码输入验证一下我看一下您能还记录好吗",
            "start_time": "46.25",
            "end_time": "57.10"
        },
        {
            "target": "客户",
            "speech": "你们就剩一点",
            "start_time": "57.10",
            "end_time": "59.01"
        },
        {
            "target": "坐席",
            "speech": "别人存都没有问题您稍等我帮您看一下",
            "start_time": "59.01",
            "end_time": "64.44"
        },
        {
            "target": "客户",
            "speech": "aa",
            "start_time": "64.44",
            "end_time": "65.07"
        },
        {
            "target": "坐席",
            "speech": "您的账单的话是三万八千六百五十九块六毛七之前还了有两万七千六百五十九块六毛七了然后的话呢在二十八二十七号二十三点",
            "start_time": "65.07",
            "end_time": "82.94"
        },
        {
            "target": "客户",
            "speech": "我想换张卡",
            "start_time": "82.94",
            "end_time": "84.53"
        },
        {
            "target": "坐席",
            "speech": "是还了一个一万一没错这个款项呢是结算的话呢由于只是原因的话的话到二十八号的一个这边的话呢也算入账所以您这边的话账单里面显示你没有还清但实际上的话您是已经还清了不用再还了三十一号您放心",
            "start_time": "84.53",
            "end_time": "113.56"
        },
        {
            "target": "客户",
            "speech": "唉你们这个什么这样查都看的我那我得干的查了好一阵花了它它不有一个叫是拿我的倒数对答都我都明明还清了怎么还",
            "start_time": "113.56",
            "end_time": "130.15"
        },
        {
            "target": "坐席",
            "speech": "给您添麻烦了非常抱歉因为您这个是还款时间的话呢比较晚的一个情况导致这边的话呢一个入账时间的话呢也可以给您添麻烦了",
            "start_time": "130.15",
            "end_time": "148.01"
        },
        {
            "target": "客户",
            "speech": "我刚才查了刚才显示的要还款一万多一万吧",
            "start_time": "148.01",
            "end_time": "154.07"
        },
        {
            "target": "坐席",
            "speech": "您不用担心嗯您看您可用额度现在的话已经有三万八千一百六十六块七毛三了已经还清了您放心的",
            "start_time": "154.07",
            "end_time": "167.79"
        },
        {
            "target": "客户",
            "speech": "噢那你们的系统怎么都没了消费下班了呢",
            "start_time": "167.79",
            "end_time": "173.53"
        },
        {
            "target": "坐席",
            "speech": "给您添麻烦了非常抱歉",
            "start_time": "173.53",
            "end_time": "176.72"
        }
    ]
    topic = '现金分期'
    # word2vec,levenshteinStr
    result = key_point.run_levenshtein(dialog, topic)
    print(result)
