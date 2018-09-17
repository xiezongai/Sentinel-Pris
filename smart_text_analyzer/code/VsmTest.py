import Levenshtein
import re
from .SentenceSplitTest import *


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
    return result if result else None



'''
sentence = "你好我是好人你也是好人吗如果是那就太好了"
sentence_list = sentenceSplit(sentence, 5, 1) 
simlist = ["你好我是好人","你也是好人吗","如果是那就太好了","你好我是好人那就太好了"]
a = levenshteinList(sentence_list, simlist, 0.5)
print(a)
'''