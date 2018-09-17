"""
计算对话分类的准确率:(acc_all:19个标签,top5)
"""
import json
import pandas

dialog = pandas.read_csv('../data/data.csv', sep='\t')
dialog_id = list(dialog['dialog_id'])
dialog_label = list(dialog['second_label'])
id_label = zip(dialog_id, dialog_label)
dialog_labels = []
for each in id_label:
    dialog_labels.append([str(each[0]), each[1]])

def get_result(path):
    """
    读出分类结果
    :return  :{"1":[[["第一个对话的第一句话", "第一个对话第一句话的匹配句1", 0.9, "标签1"],
                ["第一个对话的第一句话", "第一个对话第一句话的匹配句2", 0.8, "标签2"],
                ["第一个对话的第一句话", "第一个对话第一句话的匹配句3", 0.7, "标签3"],
                ["第一个对话的第一句话", "第一个对话第一句话的匹配句4", 0.6, "标签4"],
                ["第一个对话的第一句话", "第一个对话第一句话的匹配句5", 0.5, "标签5"]],
               [["第一个对话的第二句话", "第一个对话的第二句话的匹配句1", 0.5, "标签6"],
                ["第一个对话的第二句话", "第一个对话的第二句话的匹配句2", 0.6, "标签7"],
                ["第一个对话的第二句话", "第一个对话的第二句话的匹配句3", 0.7, "标签8"],
                ["第一个对话的第二句话", "第一个对话的第二句话的匹配句4", 0.8, "标签9"]]],
        "2":[[["第二个对话的第一句话", "第二个对话第一句话的匹配句1", 0.5, "标签10"],["第二个对话的第一句话", "第二个对话第一句话的匹配句2", 0.5, "标签11"]]]}
    """
    with open(path, 'r', encoding='utf8') as f:
        result = json.loads(f.read())
    return result

def calculate_accuracy(result):
    """
    计算19个label的准确率
    :param result: {"1": [[("原句", "匹配句", 0.8, "查询资料"), ("原句1", "匹配句1", 0.8, "标签2"), ...]]}
    :return: acc <float>:0.7准确率
    """
    labels53 = ['中间业务营销类投诉', '标志代码', '设置卡片限额', '产品预约', '额度查询', '设置密码', '解除标志', '查询/修改账单方式', '销卡业务', '已出账单', '调额婉拒',
                '年费产品', '卡转卡办理', '分期类投诉', '还款未入账处理', '现金分期', '账单补寄', '卡片挂失', '中收产品', '用卡服务', '交易模式', '还款方式查询', '邮购分期',
                '管控项目', '财务费用查询', '延期还款', '收费标准', '未出账单', '自动转账及购汇', '商场分期', '电邮传真变更信息', '专项额度', '止付业务', '卡片激活', '换卡业务',
                '圆梦金大额消费分期', '查询/修改账单日', '微产品', '开具证明', '溢缴款办理', '分期提前缴款', '中间业务类取消', '总欠款查询', '还款查询', '征信记录', '查询个人资料',
                '上载标志', '修改个人资料', '费用减免', '额度调整', '附属卡营销', '账单/单笔分期', '疑似欺诈处理']
    labels19 = ['设置密码', '解除标志', '调额婉拒', '年费产品', '卡转卡办理', '现金分期', '卡片挂失', '中收产品', '交易模式', '延期还款', '自动转账及购汇', '卡片激活',
                '圆梦金大额消费分期', '微产品', '溢缴款办理', '额度调整', '账单单笔分期', '账单查询', '分期提前缴款']
    labels24 = ["微产品", "额度调整", "调额婉拒", "卡片挂失", "交易模式", "解除标志", "卡转卡办理", "卡片激活", "年费产品", "设置密码", "现金分期", "延期还款", "溢缴款办理",
                "圆梦金大额消费分期", "查询/修改账单日", "已出账单", "未出账单", "总欠款查询", "查询/修改账单方式", "账单补寄", "财务费用查询", "账单/单笔分期", "中收产品",
                "自动转账及购汇", "分期提前缴款"]
    new_label = '账单查询'
    to_one = ["查询/修改账单日", "已出账单", "未出账单", "总欠款查询", "查询/修改账单方式", "账单补寄", "财务费用查询"]

    count = 0
    total = 0
    for dialog_label in dialog_labels:
        dialog_id, label = dialog_label
        labels = []
        if dialog_id in result and label in labels24:
            total += 1
            for eachsentence in result[dialog_id]:
                for itemmatched in eachsentence:
                    if itemmatched[-1] == '账单单笔分期':
                        labels.append('账单/单笔分期')
                    else:
                        labels.append(itemmatched[-1])
        if label in to_one:
            if new_label in labels:
                count += 1
        elif label in labels:
            count += 1
    acc = count/total
    return acc

if __name__ == "__main__":
    path = './result_top5.json'
    result = get_result(path)
    acc = calculate_accuracy(result)
    print("acc_top5: ",acc)