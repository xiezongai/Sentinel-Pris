# encoding=utf-8
import datetime
s = "答非所问\n(没|不)(懂|理解|知道)\n你说什么\n重复.*?一遍\n(不明白|不理解).*?(吗|吧)\n(说|讲).*不明白\n回答.*?问题\n对牛弹琴\n打马虎眼\n费劲\n再.*?(回答|重复)\n你.*?有问题\n(听|说|解释).*?(没|不)清楚\n糊涂\n你.*?新来的\n[^是]不是这个意思\n乱七八糟的\n换.人接\n没听懂\n能听到吗"
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # str
print(type(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
for i in s.split('\n'):
    print(i)
