'''
用对话和匹配库得到匹配结果(result_top5.json)
'''
import time
from utils2 import *
from calculate_accuracy_19 import *

def run(data, corpus, path):
    '''
    对data进行匹配，使用corpus匹配库，将结果保存到路径path
    匹配结果最多一句话有五个标签
    :param data: [['第一个对话的第一句话', '第一个对话的第二句话'],['第二个对话'],[],...]
    :param corpus:  {"标签一":["第一句语料","第二句语料"], "":[], ...}
    :param path: ‘./result.json’
    :return: 打印出准确率,保存结果到path
    '''
    time0 = time.time()
    threshold = 0.8
    N = 5
    result={}
    i = 0
    for eachdialog in data:
        print(i)
        # print(eachdialog)
        dialog_matched = []
        for eachsentence in eachdialog:
            if eachsentence == '':
                pass
            else:
                sentence_matched=[]
                topN = []
                for eachcorpus in corpus.items():
                    topic = eachcorpus[0]
                    simlist = eachcorpus[1]
                    sim_temp_list = levenshteinList(eachsentence, simlist, threshold)
                    if sim_temp_list:
                        score = sim_temp_list[0]
                        if len(topN) <= N:
                            topN.append(score)
                            sentence_matched.append([sim_temp_list[1], sim_temp_list[2], score, topic])
                        elif score > min(topN):
                            sentence_matched.append([sim_temp_list[1], sim_temp_list[2], score, topic])
                            for item in sentence_matched:
                                if item[2] == min(topN):
                                    sentence_matched.remove(item)
                                    break
                if sentence_matched != []:
                    dialog_matched.append(sentence_matched)
        result[dialog_id[i]]=dialog_matched
        i += 1

    time1 = time.time()
    with open(path, 'w') as f:
        json.dump(result, f, ensure_ascii=False)
    cost = time1 -time0
    return cost

if __name__=='__main__':
    data = data('../data/dialog_original.json')
    corpus = corpus('../data/corpus_original.json')
    path = './result_top5_2.json'
    cost = run(data, corpus, path)
    print('time for processing:', cost, ', that is:', round(cost/60/60, 2), 'hours')