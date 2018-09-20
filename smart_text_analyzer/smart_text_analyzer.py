import pandas as pd
import re
import json

MAX_RESULT = 10


class SmartTextAnalyzer:
    def __init__(self, id, name, description, target, matched_sentences, threshold, regex, mode, created_datetime):
        """
        @Description: 创建一个SmartTextAnalyzer instance
        @param id: str
        @param name: str, "辱骂指责"
        @param description: str, 解释信息
        @param target: str, 只有三种取值 "all" "坐席" "客户"
        @param matched_sentences: [str,str], 用户输入的匹配句，注意是一个list
        @param threshold: float, 句子相似度算法的阈值
        @param regex: [str,str], 正则表达式的pattern
        @param mode: str, 目前有三种取值: all,levenshtein,regex
        @param created_datetime: str
        @Return: None
        """
        self.id = id
        self.name = name
        self.description = description
        self.target = target  # all,坐席,客户
        self.matched_sentences = matched_sentences  # [str,str]
        self.threshold = threshold
        self.regex = regex   # [str,str]
        self.mode = mode
        self.created_datetime = created_datetime  

    def run_regex(self, transcripts, dialog_id):
        """
        @Description: 针对于单个text analyzer做测试,只测试一个对话
        @param  transcripts: [{"speech": "坐席 or 客户", "target": <string>, "start_time": <string>, "end_time": <string>}]
        @param  dialog_id:str
        @return {
                "id": "",
                "target": "", # 说话者身份
                "matched": [             # 如果没有匹配到任何句子，则返回的matched字段为[]
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
        result = {"id": dialog_id, "target": self.target, "matched": []}
        for sentence in transcripts:
            if self.target == "all":
                for reg in self.regex:
                    if re.search(reg, sentence["speech"]):
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
                        break
                continue
            elif self.target == "坐席" and sentence["target"] == "坐席":
                for reg in self.regex:
                    if re.search(reg, sentence["speech"]):
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
                        break
                continue
            elif self.target == "客户" and sentence["target"] == "客户":
                for reg in self.regex:
                    if re.search(reg, sentence["speech"]):
                        result["matched"].append(
                            {"score": 1, "source": sentence["speech"], "matched": "", "start_time": sentence["start_time"], "end_time": sentence["end_time"], "origin": sentence["speech"], "regex": reg})
                        break
                continue
        return result

    def test(self, dialogs):
        '''
        测试多个对话  # TODO 多种算法合并结果
        @param dialogs : [{"transcripts": [{},{}], "id": str}, {"transcripts": [{},{}], "id": str}]
        @return 只返回matched到的对话,如果没有匹配的对话，则返回[]:[{
            "id": str,
            "matched": [
                    {
                        "score": 0.5454545454545454,  # 对于regex, score=1
                        "source": "没有了",            # 对话句子（切割之后）
                        "matched": "",                # 匹配句
                        "start_time": "08:06:38",
                        "end_time": "08:06:43",
                        "origin": "没有了没有了",       # 对话句子（未切割）
                        "regex": ""                    # regex pattern
                    }],
            "transcripts": str(dumped),
            "target": str
            }]
        '''
        matched = []
        for dialog in dialogs:
            result = self.run_regex(transcripts=dialog["transcripts"], dialog_id=dialog["id"])
            if len(result['matched']):
                matched.append({
                    "id": dialog['id'],
                    "target": self.target,
                    "matched": result["matched"],
                    "transcripts": json.dumps(dialog["transcripts"], ensure_ascii=False)
                })
            if len(matched) == MAX_RESULT:  # TODO 仅供测试，只测试MAX_RESULT个对话
                return matched
        return matched


if __name__ == '__main__':
    # 每一个text analyzer都对应着一个SmartTextAnalyzer instance，应该在后台服务启动的时候根据db创建所有的text analyzer
    classifier = SmartTextAnalyzer(id="sfrer", name='答非所问', description="", target="客户", matched_sentences=None, threshold=0.8, regex=[], mode=[], created_datetime=None)

    # 测试单个对话，仅供测试，实际部署不要使用该方法，而是test
    transcripts = [{"speech": "不知道你在说什么?", "target": "客户", "start_time": "2018-09-18 00:00:00", "end_time": "2018-09-18 00:00:00"}]
    result = classifier.run_regex(transcripts=transcripts, dialog_id="1")
    print("单个对话：", result, '\n')

    # 测试多个对话
    dialogs = [{"transcripts": transcripts, "id": "1"}, {"transcripts": transcripts, "id": "2"}]
    print("多个对话：", classifier.test(dialogs=dialogs))