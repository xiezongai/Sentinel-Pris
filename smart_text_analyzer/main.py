'''
调用class interface，以及从DB中读取模型
'''
from smart_text_analyzer import SmartTextAnalyzer

import sys
sys.path.append("..")
from database.dao.smart_text_analyzer_dao import SmartTextAnalyzerDAO
from database.dao.dialogs_dao import DialogsDAO

if __name__ == '__main__':

    # 从dialogs表中读对话
    dialogs = DialogsDAO.load_dialogs(start_time_s="2018-07-31 00:00:00", end_time_s="2018-08-01 00:00:00")
 
    # 每一个text analyzer都对应着一个SmartTextAnalyzer instance，应该在后台服务启动的时候根据db创建所有的text analyzer

    # 查看所有的SmartTextAnalyzer
    all_analyzers = SmartTextAnalyzerDAO.view_all_analyzers()  # [{id: "id", name: "name"}]
    text_analyzer = {}
    for analyzer in all_analyzers:
        id = analyzer["id"]
        name = analyzer["name"]
        analyzer = SmartTextAnalyzerDAO.view_analyzer_by_id(analyzer_id=id)
        # print("%s regex:" % name, analyzer["regex"])
        # exit()
        text_analyzer[name] = SmartTextAnalyzer(id=id, name=name, description=analyzer["description"], 
                                                target=analyzer["target"],matched_sentences=analyzer["matched_sentences"], 
                                                threshold=analyzer["threshold"], regex=analyzer["regex"], mode=analyzer["mode"], 
                                                created_datetime=analyzer["created_datetime"])

    # for name in text_analyzer:
    #     # 测试单个对话，仅供测试，实际部署不要使用该方法，而是test
    #     transcripts = [{"speech": "不知道你在说什么?", "target": "客户",
    #                     "start_time": "2018-09-18 00:00:00", "end_time": "2018-09-18 00:00:00"}]
    #     print("%s regex:" % text_analyzer[name].regex)
    #     result = text_analyzer[name].run_regex(transcripts=transcripts, dialog_id="1")
    #     print("%s--单个对话测试：" % name, result)

    #     # 测试多个对话
    #     dialogs = [{"transcripts": transcripts, "id": "1"},
    #                {"transcripts": transcripts, "id": "2"}]
    #     print("%s--多个对话测试：" % name, text_analyzer[name].test(dialogs=dialogs), '\n')

    #     exit()

    # 测试从DB中读对话，然后用text_analyzer检测
    for name in text_analyzer:
        print("%s--多个对话测试：" % name, text_analyzer[name].test(dialogs=dialogs), '\n')

        exit()