import pandas as pd
import re


class SmartTextAnalyzer:
    def __init__(self, name, target):
        self.name = name
        self.corpus_reg = {
            "用心超越期望": ['服务.*?很好', '服务.*?满意', '声音.*?好听', '说话.*?好听', '态度.*?好', '表扬', '服务.*?到位', '点.*?赞', '感谢', '服务.*?周到', '服务.*?不错', '态度.*?不错', '你很好', '声音.*?甜',
                       '说话.*?甜', '声音.*?温柔', '说话.*?温柔', '声音.*?甜', '说话.*?甜', '服务.*?满分', '细心', '服务.*?棒', '有耐心', '给.*?好评', '谢.*?服务', '你挺好', '你.*?优秀', '服务.*?积极', '五星评价', '非常专业'],
            "推诿": ['办理不了', '处理不了', '我不知道',
                   '帮不(到|了)', '我们没有.*?', '重新(致|来)电', '我不清楚', '这个问题你', '不归我们.*?'],
            "答非所问": ['答非所问', '(没|不)(懂|理解)', '你说什么', '重复.*?一遍', '(不明白|不理解).*?(吗|吧)', '(说|讲).*不明白', '回答.*?问题',
                     '你.*?到底', '对牛弹琴', '打马虎眼', '费劲', '再.*?(回答|重复)', '你.*?有问题', '(听|说|解释).*?(没|不)清楚', '糊涂', '你.*?新来的']
        }
        self.text_analyzer_reg = self.corpus_reg[self.name]
        self.target = target 

    def get_dialog(self):
        '''
        :return:
        dialog(完整对话):{"id":['有什么可以帮你','我想办一张卡','好的,请问名字是什么','你叫我小刘把']}
        dialog_service(客服的话):{"id":['有什么可以帮你','好的,请问名字是什么']}
        dialog_user(客户的话):{"id":['我想办一张卡','你叫我小刘把']}
        '''
        data = pd.read_csv('../data/data.csv', sep='\t')
        dialogs = data[['dialog_id', 'content']]
        dialog = {}
        dialog_user = {}
        dialog_service = {}
        for i in range(len(dialogs)):
            dialog_id = dialogs['dialog_id'][i]
            content = dialogs['content'][i].split('\\n')
            dialog[str(dialog_id)] = []
            dialog_user[str(dialog_id)] = []
            dialog_service[str(dialog_id)] = []
            for sentence in content:
                sentence = sentence.split('\\t')
                dialog[str(dialog_id)].append(sentence[3])
                if sentence[0] == 'customer_service':
                    dialog_service[str(dialog_id)].append(sentence[3])
                else:
                    dialog_user[str(dialog_id)].append(sentence[3])
        return dialog, dialog_service, dialog_user

    def get_corpus_reg(self):
        corpus_reg = {}
        corpus_reg['用心超越期望'] = ['服务.*?很好', '服务.*?满意', '声音.*?好听', '说话.*?好听', '态度.*?好', '表扬', '服务.*?到位', '点.*?赞', '感谢', '服务.*?周到', '服务.*?不错', '态度.*?不错', '你很好', '声音.*?甜',
                                '说话.*?甜', '声音.*?温柔', '说话.*?温柔', '声音.*?甜', '说话.*?甜', '服务.*?满分', '细心', '服务.*?棒', '有耐心', '给.*?好评', '谢.*?服务', '你挺好', '你.*?优秀', '服务.*?积极', '五星评价', '非常专业']
        corpus_reg['推诿'] = ['办理不了', '处理不了', '我不知道',
                            '帮不(到|了)', '我们没有.*?', '重新(致|来)电', '我不清楚', '这个问题你', '不归我们.*?']
        corpus_reg['答非所问'] = ['答非所问', '(没|不)(懂|理解)', '你说什么', '重复.*?一遍', '(不明白|不理解).*?(吗|吧)', '(说|讲).*不明白', '回答.*?问题',
                              '你.*?到底', '对牛弹琴', '打马虎眼', '费劲', '再.*?(回答|重复)', '你.*?有问题', '(听|说|解释).*?(没|不)清楚', '糊涂', '你.*?新来的']
        return corpus_reg[self.name]

    def run_regex(self, transcripts, dialog_id):
        """
        @Description: 针对于单个text analyzer做测试,只测试一个对话
        @param  transcripts: [{"speech": "坐席 or 客户", "target": <string>, "start_time": <string>, "end_time": <string>}]
        @param  dialog_id:str
        @return {
                "dialog_id": "",
                "matched": [
                    {
                        "score": 0.5454545454545454,  # 对于regex, score=1
                        "source": "没有了",            # 对话句子  
                        "matched": "",                # 保持格式一致，此处置空
                        "start_time": "08:06:38",
                        "end_time": "08:06:43",
                        "origin": "没有了没有了",       # 对话句子，与source保持一致
                        "regex": ""                    # regex pattern
                    }
                ]
            }
        """
        result = {"dialog_id": dialog_id, "matched": []}
        for sentence in transcripts:
            if self.target == "all":
                for reg in self.text_analyzer_reg:
                    if re.search(reg, sentence["speech"]):
                        # 匹配结果有四项['我想办张卡','办.*?卡',1,办卡业务]
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
            if self.name in ['推诿'] and sentence["target"] == "坐席":  # 推诿只对坐席的话进行匹配
                for reg in self.text_analyzer_reg:
                    if re.search(reg, sentence["speech"]):
                        # 匹配结果有四项['我想办张卡','办.*?卡',1,办卡业务]
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
            elif self.name in ['用心超越期望', '答非所问'] and sentence["target"] == "坐席"
        # 正则表达式匹配结果
        dialog, dialog_service, dialog_user = self.get_dialog()
        if self.name in ['推诿']:
            dialog = dialog_service  # 推诿只对客服的话进行匹配
        elif self.name in ['用心超越期望', '答非所问']:
            dialog = dialog_user  # 只对客户的话进行匹配
        corpus_reg = self.get_corpus_reg()
        result = {}  # {'1':[['我想办张卡','办.*?卡',1,办卡业务]], '2':[]}
        for dialog_id, content in dialog.items():
            result[dialog_id] = []
            for sentence in content:
                for reg in corpus_reg:
                    if re.search(reg, sentence):
                        # 匹配结果有四项['我想办张卡','办.*?卡',1,办卡业务]
                        result[dialog_id].append(
                            [sentence, reg, 1, self.name])

        return result


if __name__ == '__main__':
    classifier = SmartTextAnalyzer('答非所问')
    result = classifier.run_regex()
    print(result)
