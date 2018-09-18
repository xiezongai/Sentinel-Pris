import pandas as pd
import re
import json

MAX_RESULT = 50


class SmartTextAnalyzer:
    def __init__(self, name, target):
        self.name = name  
        self.corpus_reg = {
            "用心超越期望": ['服务.*?很好', '服务.*?满意', '声音.*?好听', '说话.*?好听', '态度.*?好', '表扬', '服务.*?到位', '点.*?赞', '感谢', '服务.*?周到', '服务.*?不错', '态度.*?不错', '你很好', '声音.*?甜',
                       '说话.*?甜', '声音.*?温柔', '说话.*?温柔', '声音.*?甜', '说话.*?甜', '服务.*?满分', '细心', '服务.*?棒', '有耐心', '给.*?好评', '谢.*?服务', '你挺好', '你.*?优秀', '服务.*?积极', '五星评价', '非常专业'],
            "推诿": ['办理不了', '处理不了', '我不知道',
                   '帮不(到|了)', '我们没有.*?', '重新(致|来)电', '我不清楚', '这个问题你', '不归我们.*?'],
            "答非所问": ['答非所问', '(没|不)(懂|理解|知道|明白|清楚)', '你说什么', '重复.*?一遍', '(不明白|不理解).*?(吗|吧)', '(说|讲).*不明白', '回答.*?问题',
                     '你.*?到底', '对牛弹琴', '打马虎眼', '费劲', '再.*?(回答|重复)', '你.*?有问题', '(听|说|解释).*?(没|不)清楚', '糊涂', '你.*?新来的']
        }
        self.text_analyzer_reg = self.corpus_reg[self.name]
        self.target = target  # all,坐席,客户

    def run_regex(self, transcripts, dialog_id):
        """
        @Description: 针对于单个text analyzer做测试,只测试一个对话
        @param  transcripts: [{"speech": "坐席 or 客户", "target": <string>, "start_time": <string>, "end_time": <string>}]
        @param  dialog_id:str
        @return {
                "dialog_id": "",
                "target": "", # 说话者身份
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
        result = {"dialog_id": dialog_id, "target": self.target, "matched": []}
        for sentence in transcripts:
            if self.target == "all":
                for reg in self.text_analyzer_reg:
                    if re.search(reg, sentence["speech"]):
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
                continue
            elif self.target == "坐席" and sentence["target"] == "坐席":
                for reg in self.text_analyzer_reg:
                    if re.search(reg, sentence["speech"]):
                        # 匹配结果有四项['我想办张卡','办.*?卡',1,办卡业务]
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
                continue
            elif self.target == "客户" and sentence["target"] == "客户":
                for reg in self.text_analyzer_reg:
                    if re.search(reg, sentence["speech"]):
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
                continue
        return result

    def test(self, dialogs):
        '''
        测试多个对话  # TODO 多种算法合并结果
        @param dialogs : [{"transcripts": [{},{}], "dialog_id": str}, {"transcripts": [{},{}], "dialog_id": str}]
        @return 只返回matched到的对话,[{
            "dialog_id": str,
            "matched": [
                    {
                        "score": 0.5454545454545454,  # 对于regex, score=1
                        "source": "没有了",            # 对话句子  
                        "matched": "",                # 保持格式一致，此处置空
                        "start_time": "08:06:38",
                        "end_time": "08:06:43",
                        "origin": "没有了没有了",       # 对话句子，与source保持一致
                        "regex": ""                    # regex pattern
                    }],
            "transcripts": str(dumped),
            "target": str
            }]
        '''
        matched = []
        for dialog in dialogs:
            result = self.run_regex(transcripts=dialog["transcripts"], dialog_id=dialog["dialog_id"])
            if len(result['matched']):
                matched.append({
                    "dialog_id": dialog['dialog_id'],
                    "target": self.target,
                    "matched": result["matched"],
                    "transcripts": json.dumps(dialog["transcripts"], ensure_ascii=False)
                })
            if len(matched) == MAX_RESULT:  # TODO 仅供测试，只测试MAX_RESULT个对话
                return matched
        return matched


if __name__ == '__main__':
    classifier = SmartTextAnalyzer(name='答非所问', target="客户")

    # 测试单个对话
    transcripts = [{"speech": "我不知道你在说什么?", "target": "客户", "start_time": "2018-09-18 00:00:00", "end_time": "2018-09-18 00:00:00"}]
    result = classifier.run_regex(transcripts=transcripts, dialog_id="1")
    print("单个对话：", result, '\n')

    # 测试多个对话
    dialogs = [{"transcripts": transcripts, "dialog_id": "1"}, {"transcripts": transcripts, "dialog_id": "2"}]
    print("多个对话：", classifier.test(dialogs=dialogs))