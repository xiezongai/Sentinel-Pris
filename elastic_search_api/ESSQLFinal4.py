# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 10:27:15 2018

@author: xiezongai
"""
from elasticsearch import Elasticsearch

class ESSearch:
    def __init__(self,index, doc_type="doc"):
        self.es = Elasticsearch()
        self.index = index   # index name
        self.doc_type = doc_type  # 暂时不用
        
    def search_dialog_by_dialog_id(self, dialog_id):
        """
        Description: 按dialog_id进行查找
        Params: dialog_id: <string>
        Return:
        {'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15T02:33:13.000Z', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31T08:02:08.000Z', 'begin_time': '2018-07-31T07:59:07.000Z', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15T04:33:00.340Z', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07T12:41:03.000Z', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'}
        """
        body = {'query':{'match_phrase':{'dialog_id':{'query':dialog_id}}}}
        res = self.es.search(index=self.index, body=body)
        return res['hits']['hits'][0]['_source']
    
    
    def search_dialog_by_call_id(self, call_id):
        """
        Description: 按call_id进行查找
        Params: call_id: <string>
        Return:
        [{'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15T02:33:13.000Z', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31T08:02:08.000Z', 'begin_time': '2018-07-31T07:59:07.000Z', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15T04:33:00.340Z', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07T12:41:03.000Z', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'},{}...]
        """
        body = {'query':{'match_phrase':{'call_id':{'query':call_id}}}}
        res = self.es.search(index=self.index, body=body)
        return_list=[]
        for i in res['hits']['hits']:
            return_list.append(i['_source'])
        return return_list
    
    def search_dialog_by_session_id(self, session_id):
        """
        Description: 按session_id进行查找
        Params: session_id: <string>
        Return:
        [{'callee_no': '98076', 'machine_score': 0, 'updatetime': '2018-09-15T02:33:13.000Z', '@version': '1', 'caller_no': '14213', 'transcripts': 'pass', 'is_manual_rated': False, 'end_time': '2018-07-31T08:02:08.000Z', 'begin_time': '2018-07-31T07:59:07.000Z', 'silence': 0.0, 'manual_rating': '', 'id': 'f0ada676-b7b4-11e8-b833-3c404f107c90', '@timestamp': '2018-09-15T04:33:00.340Z', 'call_id': '1520948153-263390', 'emotion': '', 'created_at': '2018-09-07T12:41:03.000Z', 'interruption': '', 'manual_score': 0, 'status': 3, 'session_id': '80f705de-a1e0-11e8-a9a0-784f437148a2'},{}...]
        """
        body = {'query':{'match_phrase':{'session_id':{'query':session_id}}}}
        res = self.es.search(index=self.index, body=body)
        return_list=[]
        for i in res['hits']['hits']:
            return_list.append(i['_source'])
        return return_list
    
    def search_dialog_by_topic(self, topic):
        """
        Description: 按topic进行查找
        Params: topic: <string>
        return : [{"dialog_id": <string>, "transcripts", <string>, "topic": <string>}]
        """
        body = {'query':{'match_phrase':{'topic':{'query':topic}}}}
        res = self.es.search(index=self.index, body=body)
        return_list=[]
        return_dict={}
        for i in res['hits']['hits']:
            return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"]=i['_source']['transcripts']
            return_dict["topic"]=i['_source']['topic']
            return_list.append(return_dict)
        return return_list            
    
    def search_dialog_by_silence(self, silence_total=None, silence_max=None):
        """
        Description:返回大于silence_total或者silence_max的信息
        Params:silence_total,silence_max : <float>  
        return : [{"dialog_id":<string>, "transcripts": <string>, "silence_total":<float>, "silence_max":<float>}]
        """
        if silence_total and silence_max:
            body = {"query": { "bool": {"must":[{"range": {'silence_total': {"gte": silence_total}}},{"range": {'silence_max': {"gte": silence_max}}}]}}}
        elif not silence_total and silence_max:
            body = {"query": { "range": {'silence_max': {"gte": silence_max}}}}
        elif not silence_max and silence_total:
            body = {"query": { "range": {'silence_total': {"gte": silence_total}}}}
        res = self.es.search(index=self.index, body=body)
        return_list=[]
        return_dict={}
        for i in res['hits']['hits']:
            return_dict["dialog_id"]=i['_source']['dialog_id']
            return_dict["transcripts"]=i['_source']['transcripts']
            return_dict["silence_total"]=i['_source']['silence_total']
            return_dict["silence_max"]=i['_source']['silence_max']
            return_list.append(return_dict)
        return return_list     
    
    def search_dialog_by_text_1(self, sentence, mode="fuzzy"):
        """
        Description:返回模糊匹配到的对话以及高亮部分
        Params:sentence:<string> 
        Return:
        [{'transcripts':<string>,'highlight':<string>},{}...]
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
        return_dict={}
        return_list=[]
        for i in res['hits']['hits']:
            return_dict["transcripts"]=i['_source']['transcripts']
            return_dict["highlight"]=i['highlight']
            return_list.append(return_dict)
        return return_list
        
    def search_dialog_by_text_2(self, sentence="", mode="accurate"):
        """
        Description:返回模糊匹配到的对话以及高亮部分
        Params:sentence:<string> 
        Return:
        [{'transcripts':<string>,'highlight':<string>},{}...]
        """
        body = {'query':{'match_phrase':{'transcripts':{'query':sentence}}},
                "highlight": {"fields": {"transcripts": {"pre_tags": [""],"post_tags": [""]}}}}
        res = self.es.search(index=self.index, body=body)
        return_dict={}
        return_list=[]
        for i in res['hits']['hits']:
            return_dict["transcripts"]=i['_source']['transcripts']
            return_dict["highlight"]=i['highlight']
            return_list.append(return_dict)
        return return_list        
        

    
if __name__ == '__main__': 
    ESSearch= ESSearch('dialogs')  
    #ESSearch.search_dialog_by_dialog_id()#缺少字段，无法测试
    a=ESSearch.search_dialog_by_call_id('1520948153-263390')
    b=ESSearch.search_dialog_by_session_id('80f705de-a1e0-11e8-a9a0-784f437148a2')
    #ESSearch.search_dialog_by_topic()#缺少字段，无法测试  
    #ESSearch.search_dialog_by_silence()#缺少字段，无法测试    
    c=ESSearch.search_dialog_by_text_1('现金分期的业务办理')
    d=ESSearch.search_dialog_by_text_2('噢还在这不能用那唉那我这个呃假如说你刚才算南十万就是说消费我就说柜台可以')
    print('testing search_dialog_by_call_id','\n',a,'\n')
    print('testing search_dialog_by_session_id','\n',b,'\n')
    print('testing search_dialog_by_text_1','\n',c,'\n')
    print('testing search_dialog_by_text_2','\n',d,'\n')
    
    
    
    
    
    
    
    
    
    
    
    
    