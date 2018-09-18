import json,copy
import Levenshtein
import linecache

def corpus(path):
    '''
    读取匹配库
    :param path: ‘./corpus_19.json’
    :return: {"申请办卡"：["要办卡"]}
    '''
    with open(path, 'r', encoding="utf-8")as f:
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

def levenshteinStr(sentence, simlist, threshold, model=None):
    """
    单句与匹配句子list做相似度计算，返回相似度分值最高的一个
    :param sentence:string, 原句
    :param simlist:list, 匹配句子list
    :param threshold:float, 阈值
    :return [score, source_sentence, matched_sentence]"""
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

def top_keypoint(keypoints):
    '''
    取多个关键点的top1：
    :param keypoints: list,[{'keypoint':'key1', 'score':0.2, 'compared_source':'sdd'}, {'keypoint':'key2', 'score':0.9, 'compared_source':'top1_compared_sentence'}, {'keypoint':'key3', 'score':0.6, 'compared_source':'top1_compared_sentence1'}]
    :return top1_keypoint:{'compared_source': 'top1_compared_sentence', 'keypoint': 'key2', 'score': 0.9}
    '''
    keypoint_list = [item['keypoint'] for item in keypoints]
    score = [item['score'] for item in keypoints]
    score_forindex = copy.deepcopy(score)
    score.sort()
    index = score_forindex.index(score[-1])
    top1_keypoint = keypoints[index]
    return top1_keypoint

from gensim.models import Word2Vec
import numpy as np
import jieba

def w2v_model(sentence,simi_list,threshold,model):
    '''
    :param sentence: 输入单句
    :param simi_list: 匹配库
    :param threshold: 输出相似度最大的句子的阈值
    :return: [score, source_sentence, matched_sentence]
    '''
    model_loaded = model
    words = list(jieba.cut(sentence.strip()))
    words_new=[]
    for each_slice in words:
        try:
             vocab = model_loaded[each_slice]
             words_new.append(each_slice)
        except KeyError:
            print("not in vocabulary")

    sim_temp_list = []
    sim_temp = float(threshold)
   # print(simi_list)
    for candidate in simi_list:
        score = 0
        if candidate == '':
            pass
        else:
            candidate_list = list(jieba.cut(candidate))
            try:
                score = model_loaded.n_similarity(words_new, candidate_list)
            except Exception:
                print("words_new:", words_new, "candidate_list:", candidate_list)
                exit()
            if score > sim_temp:
                sim_temp = score
                sim_temp_list = [sim_temp, sentence, candidate]
            else:
                continue
    if not sim_temp_list:
        return None
    else:
        return sim_temp_list
