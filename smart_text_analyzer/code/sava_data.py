'''
对原始数据进行过滤，保存到data_final.json
'''
from data_final import *
from utils import *
from calculate_accuracy_19 import dialog_labels
new_data_util = compose(dic, 3, 8.5, sentences)
new_text = new_data_util.get_new_text()
data = {}
i = 0
for dialog_stop in new_text:
    data[dialog_labels[i][0]] = dialog_stop
    i += 1
with open('./data_final.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)