import pandas as pd
import re

class reg_classify:
    def __init__(self, analyzer_type):
        self.analyzer_type = analyzer_type

    def get_dialog(self):
        data = pd.read_csv('../data/data.csv', sep='\t')
        dialogs = data[['dialog_id','content']]
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
        corpus_reg['用心超越期望'] = ['服务.*?很好', '服务.*?满意', '声音.*?好听', '说话.*?好听', '态度.*?好', '表扬', '服务.*?到位', '点.*?赞', '感谢', '服务.*?周到', '服务.*?不错', '态度.*?不错', '你很好', '声音.*?甜', '说话.*?甜', '声音.*?温柔', '说话.*?温柔', '声音.*?甜', '说话.*?甜', '服务.*?满分', '细心', '服务.*?棒', '有耐心', '给.*?好评', '谢.*?服务', '你挺好', '你.*?优秀', '服务.*?积极', '五星评价','非常专业']
        corpus_reg['推诿'] = ['办理不了','处理不了','我不知道','帮不(到|了)','我们没有.*?','重新(致|来)电','我不清楚','这个问题你','不归我们.*?']
        corpus_reg['答非所问'] = ['答非所问','(没|不)(懂|理解)','你说什么','重复.*?一遍','(不明白|不理解).*?(吗|吧)','(说|讲).*不明白','回答.*?问题','你.*?到底','对牛弹琴','打马虎眼','费劲','再.*?(回答|重复)','你.*?有问题','(听|说|解释).*?(没|不)清楚','糊涂','你.*?新来的']
        return corpus_reg[self.analyzer_type]

    def run(self):
        # 正则表达式匹配结果
        dialog, dialog_service, dialog_user = self.get_dialog()
        if self.analyzer_type in ['推诿']:
            dialog = dialog_service
        elif self.analyzer_type in ['用心超越期望', '答非所问']:
            dialog = dialog_user
        corpus_reg = self.get_corpus_reg()
        result = {}
        for dialog_id, content in dialog.items():
            result[dialog_id] = []
            for sentence in content:
                for reg in corpus_reg:
                    if re.search(reg, sentence):
                        result[dialog_id].append([sentence, reg])

        search_result={}
        search_result[self.analyzer_type] = []
        for item in result:
            if result[item] != []:
                search_result[self.analyzer_type].append(item)

        return result, search_result

if __name__ == '__main__':
    classifier = reg_classify('答非所问')
    result = classifier.run()
    print(result)