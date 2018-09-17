import json
import Levenshtein

def corpus(path):
    '''
    读取匹配库
    :param path: ‘./corpus_19.json’
    :return: {"申请办卡"：["要办卡"]}
    '''
    with open(path, 'r')as f:
        corpus = json.load(f)
    return corpus

def data(path):
    '''
    读取过滤后的数据
    :param path: 数据的路径:'./data_final.json'
    :return: [["想办卡","好的"], []]
    '''
    with open(path, 'r')as f:
        data = json.load(f)
    new_text = []
    for eachdialog in data.items():
        new_text.append(eachdialog[1])
    return new_text

def sentenceSplit(string, N, step):
    """
    滑动窗口：对输入字符串按照窗口大小N以步长step取出，返回字符串数组
    :param  string<string>:查一下信用卡额度
    :param  N<int>：5
    :param  step<int>：1
    :return ["查一下信用卡","一下信用卡额","下信用卡额度"]
    """
    if not string:
        return []
    if N > len(string):
        return [string]
    if N == 1:
        return string

    res = []
    point = N
    while point <= len(string):
        res.append(string[point - N: point])
        point = point + step
    return res

def levenshteinStr(sentence, simlist, threshold):
    """
    return [score, source_sentence, matched_sentence]"""
    sim_temp_list = []
    sim_temp = float(threshold)
    for eachsim in simlist:
        score = Levenshtein.ratio(eachsim, sentence)
        if score > sim_temp:
            sim_temp = score
            sim_temp_list = [sim_temp, sentence, eachsim]
        else:
            continue
    if not sim_temp_list:
        return None
    else:
        return sim_temp_list

def levenshteinList(sentence, simlist, threshold):
    sentence_list = sentenceSplit(sentence, 10, 1)
    result = []
    for eachsentence in sentence_list:
        a = levenshteinStr(eachsentence, simlist, threshold)
        if a == None:
            continue
        if result == []:
            result = a
        #print(a,result)
        if float(a[0]) > float(result[0]):
            result = a
    return result