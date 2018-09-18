def sentenceSplit(string,N,step):
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
    point  = N
    while point <= len(string):
        res.append(string[point-N : point])
        point = point + step
    return res
'''
content = "1234344"
a = sentenceSplit(content,3,1)

b = sentenceSplit(content,4,2)
print(a)
print(b)
'''
def transform(result):
    """
    对smart_topic_analyser的test的结果进行转化
    :param  result:{"analyser_id":{"dialog_id":{"status":True, "matched":[(0.8, "原句", "匹配句")]}}}
    :return iddict:{"dialog_id":[("原句", "匹配句", 0.8, "analyser_type")]}
    """
    labeldict = {}
    for itemresult in result.items():
        for id_status_matched_item in itemresult[1].items():
            sentencelist = id_status_matched_item[1]['matched']
            if not sentencelist == []:
                for eachsentence in sentencelist:
                    if (eachsentence[1]+id_status_matched_item[0]) in labeldict:
                        if float(eachsentence[0])>float(labeldict[eachsentence[1]+id_status_matched_item[0]][2][0]):
                            labeldict[eachsentence[1]+id_status_matched_item[0]] = (itemresult[0],id_status_matched_item[0],eachsentence)
                    else:
                        labeldict[eachsentence[1]+id_status_matched_item[0]] = (itemresult[0],id_status_matched_item[0],eachsentence)
    iddict = {}
    for eachsentence,sentencetuple in labeldict.items():
        if sentencetuple[1] in iddict:
            iddict[sentencetuple[1]].append((sentencetuple[2][1],sentencetuple[2][2],sentencetuple[2][0],sentencetuple[0]))
        else:
            iddict[sentencetuple[1]] = [(sentencetuple[2][1],sentencetuple[2][2],sentencetuple[2][0],sentencetuple[0])]

    return iddict

def transformtopN(results, N):
    """
    对smart_topic_analyser的test的结果进行转化,每个原句保留前N个标签
    :param  results:{"analyser_id":{"dialog_id":{"status":True, "matched":[(0.8, "原句", "匹配句", "start_time1", "end_time")]}},
                    "analyser_id1":{"dialog_id":{"status":True, "matched":[(0.7, "原句", "匹配句1", "start_time2", "end_time")]}},
                    "analyser_id2":{"dialog_id":{"status":True, "matched":[(0.6, "原句", "匹配句2", "start_time3", "end_time")]}},
                    "analyser_id3":{"dialog_id":{"status":True, "matched":[(0.5, "原句", "匹配句3", "start_time4", "end_time")]}},
                    "analyser_id4":{"dialog_id":{"status":True, "matched":[(0.9, "原句", "匹配句4", "start_time5", "end_time")]}},
                    "analyser_id5":{"dialog_id":{"status":True, "matched":[(0.9, "原句", "匹配句5", "start_time6", "end_time")]}}}
    :return iddict:{"dialog_id":[[("原句", "匹配句", 0.8, "analyser_type", "start_time1", "end_time"),
                                ("原句", "匹配句1", 0.7, "analyser_type1", "start_time2", "end_time"),
                                ("原句", "匹配句2", 0.6, "analyser_type2", "start_time3", "end_time"),
                                ("原句", "匹配句4", 0.9, "analyser_type4", "start_time5", "end_time"),
                                ("原句", "匹配句5", 0.9, "analyser_type5", "start_time6", "end_time")]]}
    """
    labeldict = {}
    for itemresult in results.items():
        # print(itemresult)
        for id_status_matched_item in itemresult[1].items():
            # print (id_status_matched_item)  # ("dialog_id", {"status":True, "matched":[(0.8, "原句", "匹配句")]})
            sentencelist = id_status_matched_item[1]['matched']  # [(0.8, "原句", "匹配句")]
            if not sentencelist == []:
                for eachsentence in sentencelist:
                    # print(itemresult[0],id_status_matched_item[0],eachsentence,eachsentence[2])
                    # if labeldict.has_key():
                    if (eachsentence[1] + id_status_matched_item[0]) in labeldict:
                        # print(eachsentence[0])
                        # print(labeldict[eachsentence[1]][2][0])
                        # if float(eachsentence[0])>float(labeldict[eachsentence[1]+id_status_matched_item[0]][2][0]):
                        topN = labeldict[eachsentence[1] + id_status_matched_item[0]][-1][3]
                        # print(topN)
                        if len(topN) < N:
                            topN.append(float(eachsentence[0]))
                            labeldict[eachsentence[1] + id_status_matched_item[0]].append(
                                (itemresult[0], id_status_matched_item[0], eachsentence, topN))
                            # print(itemresult[0],id_status_matched_item[0],eachsentence,topN) #标签，对话id， 匹配项[0.7, '联通', '联通11']，[0.8, 0.7, 0.6, 0.5, 0.4]
                        else:
                            mintopN = min(topN)
                            if float(eachsentence[0]) > mintopN:
                                topN.remove(mintopN)
                                topN.append(float(eachsentence[0]))
                                for eachlabeldict in labeldict[eachsentence[1] + id_status_matched_item[0]]:
                                    if eachlabeldict[2][0] == mintopN:
                                        labeldict[eachsentence[1] + id_status_matched_item[0]].remove(eachlabeldict)
                                        break
                                labeldict[eachsentence[1] + id_status_matched_item[0]].append(
                                    (itemresult[0], id_status_matched_item[0], eachsentence, topN))
                                # print(topN)
                            else:
                                continue
                            # labeldict[eachsentence[1]+id_status_matched_item[0]] = (itemresult[0],id_status_matched_item[0],eachsentence,eachsentence[2])
                    else:
                        # labeldict[eachsentence[1]] = (itemresult[0],id_status_matched_item[0],eachsentence)
                        # print(eachsentence[1],id_status_matched_item[0])
                        topN = [float(eachsentence[0])]
                        # print(topN)
                        labeldict[eachsentence[1] + id_status_matched_item[0]] = [
                            (itemresult[0], id_status_matched_item[0], eachsentence, topN)]
                        # print("初始化: ",labeldict[eachsentence[1]+id_status_matched_item[0]])
    # print("labeldict: ",labeldict)
    iddict = {}
    # print(len(labeldict))

    for eachsentence, sententuple in labeldict.items():
        # print(eachsentence, sententuple)
        if sententuple[0][1] in iddict:   # sententuple[0][1]=dialog_id
            l = []
            for item in sententuple:      # sententuple = [(analyser_type,dialog_id,(score,原句,匹配句,start_time,end_time),topN), ...]
                l.append((item[2][1], item[2][2], item[2][0], item[0], item[2][3], item[2][4]))
            iddict[sententuple[0][1]].append(l)
        else:
            iddict[sententuple[0][1]] = [[]]
            for item in sententuple:
                iddict[sententuple[0][1]][0].append((item[2][1], item[2][2], item[2][0], item[0], item[2][3], item[2][4]))
    return iddict