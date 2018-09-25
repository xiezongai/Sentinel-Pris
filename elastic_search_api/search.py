# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 21:26:08 2018
@author: xiezongai
"""
import json
from elasticsearch import Elasticsearch


class ESSearch:
    def __init__(self, index, doc_type="doc"):
        self.es = Elasticsearch(hosts=[{'host': '10.112.57.93', 'port': 9200}])
        self.index = index   # index name
        self.doc_type = doc_type  # 暂时不用

    def search_dialog_by_dialog_id(self, dialog_id):
        """
        Description: 按dialog_id进行查找
        Params: dialog_id: <string>
        Return:
        {'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15 02:33:13', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31 08:02:08', 'begin_time': '2018-07-31 07:59:07', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15 04:33:00', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07 12:41:03', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'}
        若无符合条件的结果则返回None
        """
        body = {'query': {'match_phrase': {'dialog_id': {'query': dialog_id}}}}
        res = self.es.search(index=self.index, body=body)
        try:
            ret = res['hits']['hits'][0]['_source']
            ret['end_time'] = ret['end_time'][:-5].replace('T', ' ')
            ret['begin_time'] = ret['begin_time'][:-5].replace('T', ' ')
        except:
            ret = None
        return ret

    def search_dialog_by_call_id(self, call_id):
        """
        Description: 按call_id进行查找
        Params: call_id: <string>
        Return:
        [{'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15 02:33:13', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31 08:02:08', 'begin_time': '2018-07-31 07:59:07', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15 04:33:00', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07 12:41:03', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'},{}...]
        若无符合条件的结果则返回空列表
        """
        body = {'query': {'match_phrase': {'call_id': {'query': call_id}}}}
        res = self.es.search(index=self.index, body=body)
        return_list = []
        for i in res['hits']['hits']:
            i['_source']['end_time'] = i['_source']['end_time'][:-
                                                                5].replace('T', ' ')
            i['_source']['begin_time'] = i['_source']['begin_time'][:-
                                                                    5].replace('T', ' ')
            return_list.append(i['_source'])
        return return_list

    def search_dialog_by_session_id(self, session_id):
        """
        Description: 按session_id进行查找
        Params: session_id: <string>
        Return:
        [{'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15 02:33:13', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31 08:02:08', 'begin_time': '2018-07-31 07:59:07', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15 04:33:00', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07 12:41:03', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'},{}...]
        若无符合条件的结果则返回空列表
        """
        body = {'query': {'match_phrase': {'session_id': {'query': session_id}}}}
        res = self.es.search(index=self.index, body=body)
        return_list = []
        for i in res['hits']['hits']:
            i['_source']['end_time'] = i['_source']['end_time'][:-
                                                                5].replace('T', ' ')
            i['_source']['begin_time'] = i['_source']['begin_time'][:-
                                                                    5].replace('T', ' ')
            return_list.append(i['_source'])
        return return_list

    def search_dialog_by_topic(self, topic):
        """
        Description: 按topic进行查找
        Params: topic: <string>
        return : [{"dialog_id": <string>, "transcripts", <string>, "topic": <string>}]
        若无符合条件的结果则返回空列表
        """
        body = {'query': {'match_phrase': {'topic': {'query': topic}}}}
        res = self.es.search(index=self.index, body=body)
        return_list = []
        return_dict = {}
        for i in res['hits']['hits']:
            return_dict["dialog_id"] = i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["topic"] = i['_source']['topic']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_silence(self, silence_total=None, silence_max=None):
        """
        Description:返回大于silence_total或者silence_max的信息
        Params:silence_total,silence_max : <float>  
        return : [{"dialog_id":<string>, "transcripts": <string>, "silence_total":<float>, "silence_max":<float>}]
        若无符合条件的结果则返回空列表
        """
        if silence_total and silence_max:
            body = {"query": {"bool": {"must": [{"range": {'silence_total': {
                "gte": silence_total}}}, {"range": {'silence_max': {"gte": silence_max}}}]}}}
        elif not silence_total and silence_max:
            body = {"query": {"range": {'silence_max': {"gte": silence_max}}}}
        elif not silence_max and silence_total:
            body = {"query": {"range": {'silence_total': {"gte": silence_total}}}}
        res = self.es.search(index=self.index, body=body)
        return_list = []
        return_dict = {}
        for i in res['hits']['hits']:
            return_dict["dialog_id"] = i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["silence_total"] = i['_source']['silence_total']
            return_dict["silence_max"] = i['_source']['silence_max']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_time_range(self, timestart, timeend):
        """
        Description: 返回符合时间要求的索引内容
        Params: timestart,timeend:<string>  例:'2018-09-15 01:01:01'
        Return:
        [{'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15 02:33:13', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31 08:02:08', 'begin_time': '2018-07-31 07:59:07', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15 04:33:00', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07 12:41:03', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'},{}...]
        若无符合条件的结果则返回空列表
        """
        timestart = timestart.split(' ')
        timestart = timestart[0] + 'T' + timestart[1] + '.000Z'
        timeend = timeend.split(' ')
        timeend = timeend[0] + 'T' + timeend[1] + '.000Z'
        body = {"query": {"bool": {"must":
                                   [{"range": {'begin_time': {"gt": timestart}}},
                                    {"range": {'end_time': {"lt": timeend}}}]}}}
        res = self.es.search(index=self.index, body=body)
        return_list = []
        for i in res['hits']['hits']:
            i['_source']['end_time'] = i['_source']['end_time'][:-
                                                                5].replace('T', ' ')
            i['_source']['begin_time'] = i['_source']['begin_time'][:-
                                                                    5].replace('T', ' ')
            return_list.append(i['_source'])
        return return_list

    def search_dialog_by_text_1(self, sentence, mode="fuzzy"):
        """
        Description:返回模糊匹配到的对话以及高亮部分
        Params:sentence:<string> 
        Return:
        [{"dialog_id": <string>,'transcripts':<string>,'highlight':dict},{}...]
        若无符合条件的结果则返回空列表
        """
        body = {
            "query": {
                "match": {"transcripts": sentence}
            },
            "highlight": {
                "fields": {
                    "transcripts": {
                        "pre_tags": [""],
                        "post_tags": [""]
                    }

                }
            }
        }
        res = self.es.search(index=self.index, body=body)
        return_dict = {}
        return_list = []
        for i in res['hits']['hits']:
            # return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["highlight"] = i['highlight']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_text_2(self, sentence="", mode="accurate"):
        """
        Description:返回模糊匹配到的对话以及高亮部分
        Params:sentence:<string> 
        Return:
        [{"dialog_id": <string>,'transcripts':<string>,'highlight':dict},{}...]
        若无符合条件的结果则返回空列表
        """
        body = {'query': {'match_phrase': {'transcripts': {'query': sentence}}},
                "highlight": {"fields": {"transcripts": {"pre_tags": [""], "post_tags": [""]}}}}
        res = self.es.search(index=self.index, body=body)
        return_dict = {}
        return_list = []
        for i in res['hits']['hits']:
            # return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["highlight"] = i['highlight']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_text_3(self, sentence, logic="and", mode="fuzzy"):
        '''
        Description:按逻辑’或‘和’与‘进行组合模糊查询
        params: sentence:list of string ,logic:'and'或'or'
        Return:
        [{"dialog_id": <string>,'transcripts':<string>,'highlight':dict},{}...]
        若无符合条件的结果则返回空列表
        '''
        match_list = []
        if logic == 'and':
            bool_type = 'must'
        elif logic == 'or':
            bool_type = 'should'
        for i in sentence:
            match_list.append({'match': {'transcripts': i}})
        body = {"query": {"bool": {bool_type: match_list}},
                "highlight": {"fields": {"transcripts": {"pre_tags": [""], "post_tags": [""]}}}}
        res = self.es.search(index=self.index, body=body)
        return_dict = {}
        return_list = []
        for i in res['hits']['hits']:
            # return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["highlight"] = i['highlight']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_text_4(self, sentence, logic="and", mode="accurate"):
        '''
        Description:按逻辑’或‘和’与‘进行组合精确查询
        params: sentence:list of string ,logic:'and'或'or'
        Return:
        [{"dialog_id": <string>,'transcripts':<string>,'highlight':dict},{}...]
        若无符合条件的结果则返回空列表
        '''
        match_list = []
        if logic == 'and':
            bool_type = 'must'
        elif logic == 'or':
            bool_type = 'should'
        for i in sentence:
            match_list.append({'match_phrase': {'transcripts': {'query': i}}})
        body = {"query": {"bool": {bool_type: match_list}},
                "highlight": {"fields": {"transcripts": {"pre_tags": [""], "post_tags": [""]}}}}
        res = self.es.search(index=self.index, body=body)
        return_dict = {}
        return_list = []
        for i in res['hits']['hits']:
            # return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["highlight"] = i['highlight']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_text_5(self, sentence, mode="accurate"):
        '''
        Description:按逻辑’或‘和’与‘进行组合精确查询
        Params:sentence:{'AND':[],'OR':[],'NOT':[]}  
        Return:
        [{"dialog_id": <string>,'transcripts':<string>,'highlight':dict},{}...]
        若无符合条件的结果则返回空列表
        '''
        and_list = []
        or_list = []
        not_list = []
        for i in sentence['AND']:
            and_list.append({'match_phrase': {'transcripts': {'query': i}}})
        for i in sentence['OR']:
            or_list.append({'match_phrase': {'transcripts': {'query': i}}})
        for i in sentence['NOT']:
            not_list.append({'match_phrase': {'transcripts': {'query': i}}})
        body = {"query": {"bool": {'must': and_list, 'should': or_list, 'must_not': not_list}},
                "highlight": {"fields": {"transcripts": {"pre_tags": [""], "post_tags": [""]}}}}
        res = self.es.search(index=self.index, body=body)
        return_dict = {}
        return_list = []
        for i in res['hits']['hits']:
            # return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["highlight"] = i['highlight']
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_interuption(self, interruption=True):
        '''
        descreption:检索interuption字段
        params: interruption：True/False
        return: [{"dialog_id":<str>,"transcripts",<str>,"interruption":<str>}]
        '''
        body = {'query': {'match_phrase': {
            'interruption': {'query': interruption}}}}
        res = self.es.search(index=self.index, body=body)
        return_list = []
        return_dict = {}
        for i in res['hits']['hits']:
            return_dict["dialog_id"] = i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["interruption"] = interruption
            return_list.append(return_dict)
        return return_list

    def search_dialog_by_smart_text_analyzer(self, smart_text_analyzer):
        '''
        descreption:检索smart_text_analyzer字段，即’辱骂‘，’用心超越希望‘等七类
        params: smart_text_analyzer : str "辱骂"
        return: [{"dialog_id":<str>,"transcripts",<str>,"smart_text_analyzer": '{"analyzer_name1": "True", "analyzer_name2": "False"}'}]
        '''
        body = {'query': {'match_phrase': {'smart_text_analyzer': {
            'query': smart_text_analyzer + ': True'}}}}   # TODO 中间是否有空格
        res = self.es.search(index=self.index, body=body)
        return_list = []
        return_dict = {}
        for i in res['hits']['hits']:
            return_dict["dialog_id"] = i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict['smart_text_analyzer'] = i['_source']['smart_text_analyzer']
            return_list.append(return_dict)
        return return_list if return_list else None

    def search_dialog_by_keypoint_analyzer(self, keypoint_list, topic):
        '''
        descreption:检索keypoint_analyzer字段，即对话关键点
        params: keypoint_list:["keypoint_name1","keypoint_name2"] , topic:str
        return: [{"dialog_id":dialog_id,"transcripts",transcripts,"key_point_status": <str>(e.g. 'a: True, b: True, c: True')}]
        '''
        keypoint = []
        keypoint.append({'match_phrase': {'topic': {'query': topic}}})
        for i in keypoint_list:
            keypoint.append({'match_phrase': {'keypoint_analyzer': {'query': i + ': True'}}})  # TODO 查询错误，这个跟文本分析器不一样
        body = {"query": {"bool": {'must': keypoint}}}
        res = self.es.search(index=self.index, body=body)
        return_dict = {}
        return_list = []
        for i in res['hits']['hits']:
            return_dict["dialog_id"] = i['_source']['dialog_id']
            return_dict["transcripts"] = i['_source']['transcripts']
            return_dict["key_point_status"] = i['_source']['keypoint_analyzer']
        return_list.append(return_dict)
        return return_list

    def insertES(self, dialog_id, call_id=None, session_id=None, transcripts=None, begin_time=None, end_time=None, 
                silence_max=None, silence_total=None, emotion=None, interruption=None, topic=None, smart_text_analyzer=None, 
                keypoint_analyzer=None):
        '''
        descreption:新建索引条目，每一个条目对应一个对话的所有相关信息，包括id类、时间类、分析器类等

        params dialog_id : str
        params call_id : str
        params session_id : str
        params transcripts : str
        params begin_time : "2018-01-01 00:00:00" str
        params end_time : "2018-01-01 00:00:00" str
        params silence_max : float
        params silence_total : float
        params emotion : str, '积极'|'消极'|'中性'
        params interruption : bool
        params topic : str 业务标签
        params smart_text_analyzer : {"analyzer_name1": "True", "analyzer_name2": "False"} 所有文本分析器结果:True代表属于该分析器
        params keypoint_analyzer : ["关键点1","关键点2",...] 匹配到的所有关键点

        return: None  修改，返回一个状态值
        '''
        body = {}
        body['dialog_id'] = dialog_id  # <string>
        body['call_id'] = call_id  # <string>
        body['session_id'] = session_id  # <string>
        body['transcripts'] = transcripts  # <string>
        body['begin_time'] = begin_time  # '2018-01-01 00:00:00'
        body['end_time'] = end_time  # '2018-01-01 00:00:00'
        body['silence_max'] = silence_max  # float
        body['silence_total'] = silence_total  # float
        body['emotion'] = emotion  # <string> '积极'/'消极'/'中性'
        body['interruption'] = interruption  # <bool>   True / False
        body['topic'] = topic  # <string>
        body['smart_text_analyzer'] = json.dumps(smart_text_analyzer, ensure_ascii=False)   # <string>
        body['keypoint_analyzer'] = json.dumps(keypoint_analyzer, ensure_ascii=False)   # <string>
        self.es.index(index=self.index, doc_type=self.doc_type, body=body, params={"refresh":'true'})  # TODO 可以返回一个状态码

    def updateES(self, dialog_id, call_id=None, session_id=None, transcripts=None, begin_time=None, end_time=None, 
                silence_max=None, silence_total=None, emotion=None, interruption=None, topic=None, smart_text_analyzer=None, 
                keypoint_analyzer=None):
        '''
        descreption:更新索引条目，须填入全部字段
        params:(见下方注释)
        return: 返回一个状态值
        '''
        res = self.es.search(index=self.index, body={
            'query': {'match_phrase': {'dialog_id': {'query': dialog_id}}}
            })
        if len(res['hits']['hits']) == 0:
            return {"status": False, "message": "未查询到该dialog_id记录，请使用insertES方法新建索引项"}
        else:
            id_value = res['hits']['hits'][0]['_id']
            body = res['hits']['hits'][0]["_source"]
            body = {}
            if call_id:
                body['call_id'] = call_id  # <string>
            if session_id:
                body['session_id'] = session_id  # <string>
            if transcripts:
                body['transcripts'] = transcripts  # <string>
            if begin_time:
                body['begin_time'] = begin_time  # '2018-01-01 00:00:00'
            if end_time:
                body['end_time'] = end_time  # '2018-01-01 00:00:00'
            if silence_max:
                body['silence_max'] = silence_max  # float
            if silence_total:
                body['silence_total'] = silence_total  # float
            if emotion:
                body['emotion'] = emotion  # <string> '积极'/'消极'/'中性'
            if interruption:
                body['interruption'] = interruption  # <bool>   True / False
            if topic:
                body['topic'] = topic  # <string>
            if smart_text_analyzer:
                body['smart_text_analyzer'] = json.dumps(smart_text_analyzer, ensure_ascii=False)   # <string>
            if keypoint_analyzer:
                body['keypoint_analyzer'] = json.dumps(keypoint_analyzer, ensure_ascii=False)   # <string>
            self.es.update(index=self.index, doc_type=self.doc_type, id=id_value, body={"doc": body})


if __name__ == '__main__':
    ESSearch = ESSearch('20180922test2')
    transcripts = '[{"target": "坐席", "speech": "嗯您好什么帮到您", "start_time": "0.00", "end_time": "1.72"}, {"target": "客户", "speech": "喂你好", "start_time": "1.72", "end_time": "2.37"}, {"target": "坐席", "speech": "啊您好", "start_time": "2.37", "end_time": "3.01"}, {"target": "客户", "speech": "l这个是在这个电话服务密码的话我就没设置吧", "start_time": "3.01", "end_time": "7.53"}, {"target": "坐席", "speech": "嗯因为呢设置的话我给您语音提示设置的", "start_time": "7.53", "end_time": "11.41"}, {"target": "客户", "speech": "噢好的", "start_time": "11.41", "end_time": "12.05"}, {"target": "坐席", "speech": "那除了设伏密码还有其他业务要办吗其他", "start_time": "12.05", "end_time": "15.92"}, {"target": "客户", "speech": "唉我想咨询一下这个号我开通一个什么金额也要看一下还应该怎么填", "start_time": "15.92", "end_time": "22.38"}, {"target": "坐席", "speech": "呃我们就是呃袁梦金我们这样这个", "start_time": "22.38", "end_time": "25.61"}, {"target": "客户", "speech": "澳元目前对对想起来了", "start_time": "25.61", "end_time": "27.76"}, {"target": "坐席", "speech": "您要办一下这个对吧好简单", "start_time": "27.76", "end_time": "30.34"}, {"target": "客户", "speech": "我我就办理我一我想咨询一下我办理这个它只有白条可有募集这怎么回事这个是我已办理过的", "start_time": "30.34", "end_time": "39.16"}, {"target": "坐席", "speech": "这个业务的话是这样的就是说我们这边呢把这个我简单问一个问题我帮您介绍一下吧请问一下有没有为家人办过中信的附属卡有没有", "start_time": "39.16", "end_time": "51.65"}, {"target": "客户", "speech": "没有没有", "start_time": "51.65", "end_time": "52.51"}, {"target": "坐席", "speech": "噢好谢谢呃这个业务是这样的首先呢这个额度那我看到有三百块钱这个限额对他不占用您自己本身的一万也就是说您自己一万加上这三万的话最高可以拿十万块钱那我们这个三百块钱呢是可以分期的", "start_time": "52.51", "end_time": "71.23"}, {"target": "客户", "speech": "但我过年分期是可以我不能三十六期吧只要我动了三万可以分两分但是但是六取款对吧", "start_time": "71.23", "end_time": "79.41"}, {"target": "坐席", "speech": "对对对对", "start_time": "79.41", "end_time": "80.27"}, {"target": "客户", "speech": "噢这个利息是这个手续费是怎么算的", "start_time": "80.27", "end_time": "83.71"}, {"target": "坐席", "speech": "呃一个月一个月收的按每个月的排3G零减七五收一万块钱呢是七十五块钱", "start_time": "83.71", "end_time": "90.81"}, {"target": "客户", "speech": "噢就如果说三万块钱我分三十六期一个月是多少这就是一百多块钱是吧", "start_time": "90.81", "end_time": "97.48"}, {"target": "坐席", "speech": "前一三二八十五", "start_time": "97.48", "end_time": "98.99"}, {"target": "客户", "speech": "那每个月是二百二十五他这个每个月我再分期还的话这个一代少的话就就没有它的利息不用不少啊", "start_time": "98.99", "end_time": "108.24"}, {"target": "坐席", "speech": "它不像房贷一样会利息会越来越少的他每个月还的金额跟那个手续费是一模一样的规定的", "start_time": "108.24", "end_time": "116.63"}, {"target": "客户", "speech": "我每个月还这么多三天就是一二三四六七七还这么多对吧", "start_time": "116.63", "end_time": "122.01"}, {"target": "坐席", "speech": "可以提前还到时候可以选择", "start_time": "122.01", "end_time": "124.60"}, {"target": "客户", "speech": "我也可以提前申请还对吧", "start_time": "124.60", "end_time": "126.96"}, {"target": "坐席", "speech": "对提前还十万没还本金的百分之三收一个违约金呃后面手续费那不会再收", "start_time": "126.96", "end_time": "133.85"}, {"target": "客户", "speech": "一万块钱的一个就是七十五", "start_time": "133.85", "end_time": "136.43"}, {"target": "坐席", "speech": "啊对另外一个月是七七五", "start_time": "136.43", "end_time": "138.80"}, {"target": "客户", "speech": "然后一万块钱的分成了这分三十六期呢还是七十五对吧噢加十二期的是多少", "start_time": "138.80", "end_time": "145.90"}, {"target": "坐席", "speech": "三多少时间的话它的月利率都是一样的就是都是零点七五这月利率是不变的", "start_time": "145.90", "end_time": "153.00"}, {"target": "客户", "speech": "噢假如说我分十二期还是就是七还是七十五的手续费对吧", "start_time": "153.00", "end_time": "158.38"}, {"target": "坐席", "speech": "噢对有一万块钱就七十五块钱", "start_time": "158.38", "end_time": "161.18"}, {"target": "客户", "speech": "噢几万块钱还完就是我不是十二期也是七十五", "start_time": "161.18", "end_time": "165.48"}, {"target": "坐席", "speech": "对对对", "start_time": "165.48", "end_time": "166.13"}, {"target": "客户", "speech": "我好的我知道了", "start_time": "166.13", "end_time": "167.63"}, {"target": "坐席", "speech": "呃还有其他帮助您吗", "start_time": "167.63", "end_time": "169.57"}, {"target": "客户", "speech": "这个这个卡要查一下这个要问清楚他说现在如果就我现在就可以消费这个就要消费这个有木有对吧", "start_time": "169.57", "end_time": "178.82"}, {"target": "坐席", "speech": "对对对对对", "start_time": "178.82", "end_time": "179.90"}, {"target": "客户", "speech": "噢好的好的我知道了嗯", "start_time": "179.90", "end_time": "182.05"}, {"target": "坐席", "speech": "那还有一点的我看到您这个卡已经用了半年的了那目前您符合条件可以升级为我们银行的一个白金卡的那之前有没有接到过我们同事一个电话邀请呢", "start_time": "182.05", "end_time": "196.04"}, {"target": "客户", "speech": "没有啊", "start_time": "196.04", "end_time": "196.69"}, {"target": "坐席", "speech": "噢那没有的话也没有关系那目前那里已经在我们的一个升级的名单内的那我这边呢会将先跟您核对一下身份那没有问题的话后期我就寄一张新的白金卡过去给您用的但到时候呢呃您卡片的整体服务呢呃几点也会做一个提升好这个清楚吧", "start_time": "196.69", "end_time": "218.85"}, {"target": "客户", "speech": "这个白金卡是怎么一个网", "start_time": "218.85", "end_time": "221.22"}, {"target": "坐席", "speech": "呃白金卡的话是我们银行的一个级别非常高端每张卡片就是最高端的了那我们银行的针对目目前少部分的客户就是上海南京已经达到的是客户啊包括一个按时还款的一些客户会邀请客户办理一个白金卡来升级然后呢我", "start_time": "221.22", "end_time": "241.66"}, {"target": "客户", "speech": "癌症", "start_time": "241.66", "end_time": "242.09"}, {"target": "坐席", "speech": "卡呢", "start_time": "242.09", "end_time": "242.52"}, {"target": "客户", "speech": "白金卡还是信用卡是出去了出去了", "start_time": "242.52", "end_time": "245.75"}, {"target": "坐席", "speech": "我们这个是信用卡不是储蓄卡使用", "start_time": "245.75", "end_time": "248.98"}, {"target": "客户", "speech": "白金卡还是信用卡对吧", "start_time": "248.98", "end_time": "251.13"}, {"target": "坐席", "speech": "对还是信用卡就是在这个您目前的这个卡的基础上再升级绑上升级然后呢这个白金卡呢第一年这个年费呢是四百八那首年的感情收再从第二年开始了呃可以拿六万的积分去兑换这个年费那这个非常优惠的这个", "start_time": "251.13", "end_time": "270.71"}, {"target": "客户", "speech": "现在积分哪个地方哪里去兑啊", "start_time": "270.71", "end_time": "273.51"}, {"target": "坐席", "speech": "呃到时候这样的我们会提前三个月呃比如说现在一一般年的三月那到明年一九年的三月份要这样子为一年到时候他会提前三个月也就是说在一月份会发短信通知您呃会收年费了到时候您来个电话我们帮您兑换一下年费就可以了一万七成吧", "start_time": "273.51", "end_time": "295.89"}, {"target": "客户", "speech": "哦还有个问题就是你给我寄了一办白金卡这个卡就没用了对吧", "start_time": "295.89", "end_time": "301.70"}, {"target": "坐席", "speech": "呃我们寄一张新的卡过去给您用时候呢开通了这张卡才会作废在没有激活之前呢在邮寄的过程当中呢您的这个卡还可以正常使用的正常", "start_time": "301.70", "end_time": "314.40"}, {"target": "客户", "speech": "现在你们我收到你们那个卡给我这张卡就没用了对不对", "start_time": "314.40", "end_time": "319.56"}, {"target": "坐席", "speech": "呃收到之后还要开通才会没用没开通之前还是可以用", "start_time": "319.56", "end_time": "324.51"}, {"target": "客户", "speech": "那就是开通帮我这张卡就没用了我就要用银行卡的对吧那一张卡对吧", "start_time": "324.51", "end_time": "330.97"}, {"target": "坐席", "speech": "对对对", "start_time": "330.97", "end_time": "331.61"}, {"target": "客户", "speech": "噢那这张卡每天就是我这个今晚的钱全部转到那张卡去了对不对", "start_time": "331.61", "end_time": "337.64"}, {"target": "坐席", "speech": "对包括您的账单欠款的您的消费啊您的积分的呃全部转到这个新的白金卡上过都过来", "start_time": "337.64", "end_time": "345.60"}, {"target": "客户", "speech": "噢我知道这个调额是怎么调啊调固定额度", "start_time": "345.60", "end_time": "349.47"}, {"target": "坐席", "speech": "呃固定额度的话到时候半年到一年左右用卡时间您打个电话给我们像我们申请或者是零呃二十万款然后每个月有积分交易的话符合条件我们也会主动地帮您增加这个信用卡的额度", "start_time": "349.47", "end_time": "366.26"}, {"target": "客户", "speech": "我这个没遇到没用太看一下每个月没有允许了算了", "start_time": "366.26", "end_time": "370.99"}, {"target": "坐席", "speech": "没有没有逾期", "start_time": "370.99", "end_time": "372.28"}, {"target": "客户", "speech": "噢那如果说现在我可以申请这个固定额度啊", "start_time": "372.28", "end_time": "376.37"}, {"target": "坐席", "speech": "呃会帮您申请一下固定额度您手都喜欢一层近那麻烦输一下卡的交易密码了我验证一下", "start_time": "376.37", "end_time": "384.55"}, {"target": "客户", "speech": "嗯好的", "start_time": "384.55", "end_time": "385.19"}, {"target": "坐席", "speech": "那这边简单问题的问题不好意思第一个问题是您的奇怪是哪里的那这样几款", "start_time": "385.19", "end_time": "392.29"}, {"target": "客户", "speech": "几个什么机关是什么意思你的积分是是哪种我姓郭嘛重庆的", "start_time": "392.29", "end_time": "397.89"}, {"target": "坐席", "speech": "重庆哪里呢", "start_time": "397.89", "end_time": "398.97"}, {"target": "客户", "speech": "重庆万州", "start_time": "398.97", "end_time": "399.83"}, {"target": "坐席", "speech": "好谢谢您的十二生肖四", "start_time": "399.83", "end_time": "401.98"}, {"target": "客户", "speech": "我八十六零四十六输入啊嗯", "start_time": "401.98", "end_time": "404.56"}, {"target": "坐席", "speech": "输了嗯好谢谢呃当时登记个信诚的联系人他的电话号码是联系", "start_time": "404.56", "end_time": "410.37"}, {"target": "客户", "speech": "幺七七二三六三六八九", "start_time": "410.37", "end_time": "412.52"}, {"target": "坐席", "speech": "幺七七然后呢", "start_time": "412.52", "end_time": "413.81"}, {"target": "客户", "speech": "二十三点三", "start_time": "413.81", "end_time": "414.89"}, {"target": "坐席", "speech": "然后呢", "start_time": "414.89", "end_time": "415.54"}, {"target": "客户", "speech": "六八九九", "start_time": "415.54", "end_time": "416.40"}, {"target": "坐席", "speech": "六八九九呃", "start_time": "416.40", "end_time": "417.47"}, {"target": "客户", "speech": "呃等", "start_time": "417.47", "end_time": "417.90"}, {"target": "坐席", "speech": "陈的联系人的哦好谢谢呃您的住宅电话号码当时怎么登记呢", "start_time": "417.90", "end_time": "423.50"}, {"target": "客户", "speech": "住宅电话电话号码就是我现在没在的地方都做得也没钱的就是我这个号码吧", "start_time": "423.50", "end_time": "430.60"}, {"target": "坐席", "speech": "好的行那我明白了那我现在帮您申请一下调固定额度呃临时额度一起帮您瞧瞧帮您", "start_time": "430.60", "end_time": "438.35"}, {"target": "客户", "speech": "那好的", "start_time": "438.35", "end_time": "438.99"}, {"target": "坐席", "speech": "呃这样的现在固定额度调了一千上去到一万一然后呢再申请一个六千的临时额度到十月一号结束那调完就到一万七下了一个加了一个调到一万七的额度临时额度增加了六千规定好多添加了一天总共在原基础上多了七千块钱", "start_time": "438.99", "end_time": "459.87"}, {"target": "客户", "speech": "噢就是这个临时额度啊它到了约比方说就没有了吧好知道", "start_time": "459.87", "end_time": "465.24"}, {"target": "坐席", "speech": "ag好", "start_time": "465.24", "end_time": "465.89"}, {"target": "客户", "speech": "噢好的这个对对过年都调到一千对吧", "start_time": "465.89", "end_time": "469.33"}, {"target": "坐席", "speech": "对固定额度调一千", "start_time": "469.33", "end_time": "471.06"}, {"target": "客户", "speech": "噢就是一万一了吧h股年度的话", "start_time": "471.06", "end_time": "474.07"}, {"target": "坐席", "speech": "对", "start_time": "474.07", "end_time": "474.28"}, {"target": "客户", "speech": "噢我知道了", "start_time": "474.28", "end_time": "475.36"}, {"target": "坐席", "speech": "那我这边帮您申请一下这个盘卡地址的话还是原地址呢", "start_time": "475.36", "end_time": "480.52"}, {"target": "客户", "speech": "这是还是我去正常路桥工程有限公司吧你在还信卡我看现在不要去那个因为我们这边我的现在在公公司那边是总共是因为我的人长期的分公司这边的话就就我这个已经不行啊", "start_time": "480.52", "end_time": "496.88"}, {"target": "坐席", "speech": "可以没问题那我就按照您住的地址寄可不可以住的地", "start_time": "496.88", "end_time": "501.83"}, {"target": "客户", "speech": "我电话将它我看一下我现在以前我办过一次家的就是现在现在你给我我给你说明地址寄呢还是在我这边公司这边吧好吧", "start_time": "501.83", "end_time": "513.02"}, {"target": "坐席", "speech": "好是公司地址是吧您在公司的地址", "start_time": "513.02", "end_time": "516.25"}, {"target": "客户", "speech": "那对对对", "start_time": "516.25", "end_time": "517.11"}, {"target": "坐席", "speech": "好的您说一下地址吧我记下记下来", "start_time": "517.11", "end_time": "520.33"}, {"target": "客户", "speech": "嗯服务提示", "start_time": "520.33", "end_time": "521.41"}, {"target": "坐席", "speech": "不行", "start_time": "521.41", "end_time": "521.84"}, {"target": "客户", "speech": "休息", "start_time": "521.84", "end_time": "522.27"}, {"target": "坐席", "speech": "什么区啊", "start_time": "522.27", "end_time": "523.13"}, {"target": "客户", "speech": "因为我取新新旧的新", "start_time": "523.13", "end_time": "525.07"}, {"target": "坐席", "speech": "新旧的新湖是湖水的湖对吗", "start_time": "525.07", "end_time": "527.65"}, {"target": "客户", "speech": "因为我我我姓吴吴上面一个口下面一个天那个我们", "start_time": "527.65", "end_time": "532.38"}, {"target": "坐席", "speech": "噢我既然我对吧行", "start_time": "532.38", "end_time": "534.11"}, {"target": "客户", "speech": "啊对", "start_time": "534.11", "end_time": "534.54"}, {"target": "坐席", "speech": "然后呢", "start_time": "534.54", "end_time": "535.18"}, {"target": "客户", "speech": "用b", "start_time": "535.18", "end_time": "535.61"}, {"target": "坐席", "speech": "呃后面呢", "start_time": "535.61", "end_time": "536.47"}, {"target": "客户", "speech": "说我说放在", "start_time": "536.47", "end_time": "537.55"}, {"target": "坐席", "speech": "说是什么写这个字", "start_time": "537.55", "end_time": "539.27"}, {"target": "客户", "speech": "做一个石字一个月出来的数", "start_time": "539.27", "end_time": "541.85"}, {"target": "坐席", "speech": "一个十一个", "start_time": "541.85", "end_time": "542.93"}, {"target": "客户", "speech": "n多人你这么一页有一些输一两月的应", "start_time": "542.93", "end_time": "546.59"}, {"target": "坐席", "speech": "噢修叶的叶对吧", "start_time": "546.59", "end_time": "548.09"}, {"target": "客户", "speech": "啊啊啊对对对", "start_time": "548.09", "end_time": "549.38"}, {"target": "坐席", "speech": "就是一个耳朵旁加一个树叶的叶对吗", "start_time": "549.38", "end_time": "552.83"}, {"target": "客户", "speech": "一个石字旁石头的石", "start_time": "552.83", "end_time": "554.76"}, {"target": "坐席", "speech": "十四天啊", "start_time": "554.76", "end_time": "555.63"}, {"target": "客户", "speech": "嗯加一", "start_time": "555.63", "end_time": "556.27"}, {"target": "坐席", "speech": "其实是长是哪个时啊", "start_time": "556.27", "end_time": "558.21"}, {"target": "客户", "speech": "石头的石啊石头的石", "start_time": "558.21", "end_time": "560.14"}, {"target": "坐席", "speech": "石是石头的石吗", "start_time": "560.14", "end_time": "561.65"}, {"target": "客户", "speech": "啊对的是何时", "start_time": "561.65", "end_time": "562.94"}, {"target": "坐席", "speech": "石头的石加一个一对吧", "start_time": "562.94", "end_time": "565.09"}, {"target": "客户", "speech": "啊对", "start_time": "565.09", "end_time": "565.52"}, {"target": "坐席", "speech": "说我对八年", "start_time": "565.52", "end_time": "566.60"}, {"target": "客户", "speech": "啊对对是我说话", "start_time": "566.60", "end_time": "568.11"}, {"target": "坐席", "speech": "好稍等一下石头加一个", "start_time": "568.11", "end_time": "570.26"}, {"target": "客户", "speech": "也", "start_time": "570.26", "end_time": "570.47"}, {"target": "坐席", "speech": "好像这个字呃找到了说什么呢", "start_time": "570.47", "end_time": "573.27"}, {"target": "客户", "speech": "说换证", "start_time": "573.27", "end_time": "573.92"}, {"target": "坐席", "speech": "放是那个呃开放的放对吧", "start_time": "573.92", "end_time": "576.28"}, {"target": "客户", "speech": "好像是号码欧洲的话", "start_time": "576.28", "end_time": "578.22"}, {"target": "坐席", "speech": "嗯好那一样的然后呢后面什么地方", "start_time": "578.22", "end_time": "581.45"}, {"target": "客户", "speech": "这么发八路", "start_time": "581.45", "end_time": "582.52"}, {"target": "坐席", "speech": "正正式那个正确的正吗", "start_time": "582.52", "end_time": "584.68"}, {"target": "客户", "speech": "不是一个提什么镇镇振兴的振振兴中华的振", "start_time": "584.68", "end_time": "588.77"}, {"target": "坐席", "speech": "振兴中华的振对吧", "start_time": "588.77", "end_time": "590.49"}, {"target": "客户", "speech": "嗯这样", "start_time": "590.49", "end_time": "591.13"}, {"target": "坐席", "speech": "呃证什么路啊", "start_time": "591.13", "end_time": "592.42"}, {"target": "客户", "speech": "中华吧陆华", "start_time": "592.42", "end_time": "593.50"}, {"target": "坐席", "speech": "花", "start_time": "593.50", "end_time": "593.71"}, {"target": "客户", "speech": "好的话", "start_time": "593.71", "end_time": "594.36"}, {"target": "坐席", "speech": "挂吗", "start_time": "594.36", "end_time": "594.79"}, {"target": "客户", "speech": "发票的话对", "start_time": "594.79", "end_time": "595.87"}, {"target": "坐席", "speech": "花差的话就划走的话对吧", "start_time": "595.87", "end_time": "598.23"}, {"target": "客户", "speech": "还让我把开通划那个划", "start_time": "598.23", "end_time": "600.39"}, {"target": "坐席", "speech": "他划叉就是中华的华呢", "start_time": "600.39", "end_time": "602.54"}, {"target": "客户", "speech": "不是那个划不开的话不喜欢的话", "start_time": "602.54", "end_time": "605.55"}, {"target": "坐席", "speech": "耳东行发展的发正发路", "start_time": "605.55", "end_time": "607.70"}, {"target": "客户", "speech": "振华路", "start_time": "607.70", "end_time": "608.35"}, {"target": "坐席", "speech": "八有个数字吧对吧", "start_time": "608.35", "end_time": "610.07"}, {"target": "客户", "speech": "不是数字吧是有那个有公章发了吧", "start_time": "610.07", "end_time": "613.30"}, {"target": "坐席", "speech": "帮不是吧是是哪个吧您说不是数字吧是那个吧", "start_time": "613.30", "end_time": "617.60"}, {"target": "客户", "speech": "那就一二三四五六七八那个是语音是大写字母的那一般", "start_time": "617.60", "end_time": "622.77"}, {"target": "坐席", "speech": "噢那就八嘛就是繁体", "start_time": "622.77", "end_time": "624.70"}, {"target": "客户", "speech": "啊", "start_time": "624.70", "end_time": "624.92"}, {"target": "坐席", "speech": "好的然后", "start_time": "624.92", "end_time": "625.78"}, {"target": "客户", "speech": "六十三号", "start_time": "625.78", "end_time": "626.64"}, {"target": "坐席", "speech": "三号还有吗", "start_time": "626.64", "end_time": "627.71"}, {"target": "客户", "speech": "还有个正常路桥你后面就是一个正常路桥工程有限公公章空肚成功进行公司", "start_time": "627.71", "end_time": "634.82"}, {"target": "坐席", "speech": "可以了地址帮您改好了", "start_time": "634.82", "end_time": "636.97"}, {"target": "客户", "speech": "你哪天我用好的", "start_time": "636.97", "end_time": "638.47"}, {"target": "坐席", "speech": "地址我帮您改一下呃您好记得帮您改好的那提示一下的我们这个白金卡呢第一年是呃收一个四百八那第二年的是用六万积分兑换如果第二年您选择继续缴纳年费的话我们这张卡呢是证书的那种超申博的一个洗牙服务给您的包括一个男性的一个相应高的一个进行检测那如果第二年您选择继续缴纳年费的话呃这个超声波的一个洗牙服务还是该享受如果第二年您选择缴纳计算的话这个插上没服务就没有那我们从现在开始呢为您保留一个十天的考虑期那这个考虑七七年的那个谁时致电我们客服给我取消这订单那如果没有取消的话我们考虑结束之后就为您寄送的新卡那并且在考虑七届结束后我们才会收取年费的是白搭后续也会提示您就账单那关于这个年费的收取方式以及这个时间考虑七请问您清楚吗都可以", "start_time": "638.47", "end_time": "705.18"}, {"target": "客户", "speech": "你那个我知道了", "start_time": "705.18", "end_time": "706.69"}, {"target": "坐席", "speech": "噢您清楚对吧是的那我现在为您白金卡的一个升级以后享受我们银行的服务的那请问您是否同意办理的", "start_time": "706.69", "end_time": "716.37"}, {"target": "客户", "speech": "他可以", "start_time": "716.37", "end_time": "717.02"}, {"target": "坐席", "speech": "可以对吧哈那我们升级为白金卡之后呢呃可以享受我们白金卡的服务包括有一个航班延误险呃严我两小时的一个分期可以最高可以一千元还会有一个但我刷的保障险如果您信用卡没到账呢我们最高呢可以给三百块钱那这些服务都是可以用的那到时候我们白银卡那些白银手册一起寄过去给您以及这个使用说明书那到时候可以看到我们这个白金手册或者登录我们中信银行的官网看到这个服务的介绍那白金卡开卡之后呢第二天就会享受白金的专属服务有效时间一年如果到时候需要使用那个操作模式一样的服务呢就提前七天那之前我们二月制的一个客服热线四零零九幺九八八这个月使用那金检侧的话是没有时间限制的不用提前那本次申请白金卡的额度已经暂时维持一现在一样的您之前有没有办理过我们银行的异地行呢", "start_time": "717.02", "end_time": "785.02"}, {"target": "客户", "speech": "没异地呢", "start_time": "785.02", "end_time": "785.88"}, {"target": "坐席", "speech": "ABC是三高速的那种有办过吗", "start_time": "785.88", "end_time": "788.89"}, {"target": "客户", "speech": "我是要这么交易提示嘛对吧", "start_time": "788.89", "end_time": "791.48"}, {"target": "坐席", "speech": "呃就是呃比如说您三告诉的时候他不会有一个专员再收费吗那我不", "start_time": "791.48", "end_time": "797.72"}, {"target": "客户", "speech": "就是一期才开始就知道那个一提示音八天走的一些对吧", "start_time": "797.72", "end_time": "802.88"}, {"target": "坐席", "speech": "对对对有办过", "start_time": "802.88", "end_time": "804.17"}, {"target": "客户", "speech": "没有没有我的抹账", "start_time": "804.17", "end_time": "805.89"}, {"target": "坐席", "speech": "的话就可以了那我们这边进白金卡之后修改会作废的为了保证您修改安全呢请您把旧卡剪断的那我们白金卡对扣费后一周内会以快递EMS寄到您的一个单位地址去的那单位地址帮您改过的现在可以用的了", "start_time": "805.89", "end_time": "825.26"}, {"target": "客户", "speech": "那好好好", "start_time": "825.26", "end_time": "826.12"}, {"target": "坐席", "speech": "那另外还有一点的就是您在我们银行的还有一个叫圆梦金的业务额度按一点额度还有两万四的那这个是用于分期的有没有需要啊最近有没有大消费的一个需要", "start_time": "826.12", "end_time": "840.97"}, {"target": "客户", "speech": "这个原没不是刚才有一个三万元不行吗", "start_time": "840.97", "end_time": "844.63"}, {"target": "坐席", "speech": "您稍等您刚刚开通过对吧", "start_time": "844.63", "end_time": "847.00"}, {"target": "客户", "speech": "然后刚我看前天才开昨天还是前天开通的一个三万元问题吗不是让你给我查到的", "start_time": "847.00", "end_time": "854.53"}, {"target": "坐席", "speech": "那是这样的因为我刚刚帮您调了一下固定额度啊这种目前额度有一部分贵呃调临时额度用掉的这个", "start_time": "854.53", "end_time": "863.78"}, {"target": "客户", "speech": "我认为你查到已经四月都去了就是有目的期找你说六千打了对吧", "start_time": "863.78", "end_time": "869.81"}, {"target": "坐席", "speech": "对对对", "start_time": "869.81", "end_time": "870.45"}, {"target": "客户", "speech": "还是我开通有目前开通吧", "start_time": "870.45", "end_time": "872.82"}, {"target": "坐席", "speech": "别问金开通过的不过呢这", "start_time": "872.82", "end_time": "875.19"}, {"target": "客户", "speech": "那个", "start_time": "875.19", "end_time": "875.62"}, {"target": "坐席", "speech": "额度跟他开通了一个临时额度增加所以少了一点钱它是总的额度不变只是把", "start_time": "875.62", "end_time": "882.72"}, {"target": "客户", "speech": "那我知道", "start_time": "882.72", "end_time": "883.58"}, {"target": "坐席", "speech": "就调到您的一个呃申请临时额度去了调的", "start_time": "883.58", "end_time": "887.45"}, {"target": "客户", "speech": "噢好的", "start_time": "887.45", "end_time": "888.10"}, {"target": "坐席", "speech": "那那你办理好了还有其他帮到您吗", "start_time": "888.10", "end_time": "891.32"}, {"target": "客户", "speech": "你把那个客服密码过去对过要设置一下", "start_time": "891.32", "end_time": "894.98"}, {"target": "坐席", "speech": "服务噢好的那现在呃您设置一下六位数的电话服务密码先设置呃你好那这个业务的话已经呃电话服务密码慢一些好的了那我先看一下您现在呃这个月目前还有多少额度啊因为刚刚调整一下额度", "start_time": "894.98", "end_time": "913.06"}, {"target": "客户", "speech": "啊你给我看一下", "start_time": "913.06", "end_time": "914.57"}, {"target": "坐席", "speech": "额度还有两万四也就是说把六千的临时额度转快成这个临时额度去了把油门金", "start_time": "914.57", "end_time": "921.88"}, {"target": "客户", "speech": "我人现在就是六千", "start_time": "921.88", "end_time": "923.60"}, {"target": "坐席", "speech": "对多了六千的临时额度然后从那个三万的有没有这种都调过去但离我们近我都有两次那就零九都到了六千那用到都还是三万不变", "start_time": "923.60", "end_time": "935.65"}, {"target": "客户", "speech": "是网呃四万吧应该", "start_time": "935.65", "end_time": "937.38"}, {"target": "坐席", "speech": "三万三万的有问题嘛三万", "start_time": "937.38", "end_time": "939.74"}, {"target": "客户", "speech": "那三万元公斤", "start_time": "939.74", "end_time": "941.03"}, {"target": "坐席", "speech": "具体的一万还是有吗", "start_time": "941.03", "end_time": "942.97"}, {"target": "客户", "speech": "嗯我知道", "start_time": "942.97", "end_time": "943.83"}, {"target": "坐席", "speech": "噢好那感谢您来电了嗯再见", "start_time": "943.83", "end_time": "946.41"}, {"target": "客户", "speech": "那好的再见", "start_time": "946.41", "end_time": "947.49"}]'
#    ESSearch.insertES(id_num=1,dialog_id=2,transcripts='asdfghjkl',begin_time='2018-01-01T00:00:00.000Z',end_time='2018-01-02T00:00:00.000Z',silence_max=10.01,silence_total=123.456,call_id=1,emotion='消极',interruption=True,session_id='1',topic='现金业务',smart_text_analyzer="辱骂: True",keypoint_analyzer="a: True, b: True, c: True")
    ESSearch.updateES(dialog_id=2, transcripts=transcripts, begin_time='2018-01-01T00:00:00.000Z', end_time='2018-01-02T00:00:00.000Z', silence_max=10.01, silence_total=123.456,
                      call_id=1, emotion='消极', interruption=True, session_id='1', topic='现金业务', smart_text_analyzer="辱骂: True", keypoint_analyzer="a: True, b: True, c: True")
    a = ESSearch.search_dialog_by_call_id('1')
    b = ESSearch.search_dialog_by_session_id('1')
    ESSearch.search_dialog_by_topic('现金业务')
    ESSearch.search_dialog_by_silence(0.01, 0.1)
    c = ESSearch.search_dialog_by_text_1('现金分期的业务办理')
    d = ESSearch.search_dialog_by_text_2('嗯您好什么帮到您')
    e = ESSearch.search_dialog_by_text_3(['圆梦金', '分期', '储蓄卡'])
    f = ESSearch.search_dialog_by_text_4(['圆梦金', '分期', '储蓄卡'], logic='and')
    h = ESSearch.search_dialog_by_text_5(
        {'AND': ['圆梦金', '储蓄卡'], 'OR': ['分期'], 'NOT': ['现金']})
    g = ESSearch.search_dialog_by_time_range(
        '2017-01-01 00:00:00', '2018-07-31 09:00:00')
    print('testing search_dialog_by_call_id', '\n', a, '\n')
    print('testing search_dialog_by_session_id', '\n', b, '\n')
    print('testing search_dialog_by_text_1', '\n', c, '\n')
    print('testing search_dialog_by_text_2', '\n', d, '\n')
    print('testing search_dialog_by_text_3', '\n', e, '\n')
    print('testing search_dialog_by_text_4', '\n', f, '\n')
    print('testing search_dialog_by_text_5', '\n', h, '\n')
    print('testing search_dialog_by_time_range', '\n', g, '\n')
    i = ESSearch.search_dialog_by_dialog_id(2)
    print('testing search_dialog_by_dialog_id', '\n', i, '\n')
    j = ESSearch.search_dialog_by_seven_point_analyzer("辱骂")
    print('testing search_dialog_by_seven_point_analyzer', '\n', j, '\n')
    k = ESSearch.search_dialog_by_keypoint_analyzer(
        ['a', 'b'], '现金业务')
    print('testing search_dialog_by_keypoint_analyzer', '\n', k, '\n')
    l = ESSearch.search_dialog_by_interuption(True)
    print('testing search_dialog_by_interuption', '\n', l, '\n')
