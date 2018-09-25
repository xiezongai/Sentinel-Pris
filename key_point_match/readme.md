# Discription

针对于一个业务下的对话，检测客服是否说了某些关键点，返回关键点及对应的句子。输入是一段对话和相应的业务分类，返回这段话提到的关键点和对应的句子及句子的相关信息

代码实现了三种方法匹配关键点：
- Levenshtein
- word2vector
- regex

目前以 '现金分期'和 '设置密码'为例：

现金分期下共16个关键点

设置密码下共4个关键点：['2.提出转语音系统','3.需要登记手机号','5.确认更改消费模式/11.在线更改消费模式','13.办理成功']

# Requirements
- python3
- Levenshtein
- gensim
- numpy
- jieba

# Run
python key_point.py 

#### 调用示例：
```
key_point = KeyPoint(compare_corpus_path='data/compare_corpus_21.json') # compare_corpus_path：匹配库文件
dialog = [
            {
                "target": "坐席",
                "speech": "王先 生您好有什么可以帮您",
                "start_time": "0.00",
                "end_time": "3.83"
            },,,,
        ]
topic = '现金分期'
result = key_point.run_regex(dialog,topic) # 参数dialog:对话, topic:业务分类
```
#### main function：run_levenshtein(), run_word2vec(), run_regex()
```
Input:
    dialog: list,每一项为一个句子
            示例：[
                    {
                        "target": "坐席",
                        "speech": "王先 生您好有什么可以帮您",
                        "start_time": "0.00",
                        "end_time": "3.83"
                    },,,,
                ]
    topic:  string，业务分类
            示例：'现金分期'
    method: function，算法，该代码实现三种算法，Levenshtein，w2v_model, regex
    
Output:
    result: list, 每一项为这段话匹配到的关键点之一，
            格式：[
                                {'keypoint':'',
                                'matched':[{'sentence':'',  # 切割后的句子
                                            'compared_source':'',  # 匹配库里的原句
                                            'source_sentence':'',  # 对话中的原句（未切割）
                                            'matched_regex': "语音提示",
                                            'score': float,
                                            "start_time": "08:06:38",
                                            "end_time": "08:06:43",
                                            "regex": ''
                                            },
                                            {},,,
                                        ]
                                },
                                {},
                            ]
        '''
```

# 模块算法说明，结合具体代码实现
- 该模块以对话中的单句与匹配库中句子进行相似度匹配的方式，来完成对话中关键点的抽取
- 对于长句会进行滑窗切分成子句处理
- 单句匹配目前实现两种算法：Levenshtein和word2vector
- 默认每个句子只对应一个关键点，当匹配到多个关键点时，取相似度分值最高的一个关键点
