# Sentinel-Pris

## 代码管理规范
1. 每个模块的代码放在repo根目录的一个文件夹下，例如话术匹配新建一个huashupipei文件夹，把所有的代码放在此文件夹内。
2. 代码都放在master branch，不要新建分支。
3. 每个模块的文件夹内都应该有readme.md，包含以下内容：
    * 模块功能介绍
    * python第三方依赖库（requests.txt）: 不允许使用其它语言，如有必要，请先跟何邺沟通
    * 运行说明（要求在每个模块的文件夹下能够独立运行，写明预期的输入输出结果）
    * 模块核心代码文件介绍
    * 模块算法说明，结合具体代码实现

## 补充说明
1. 代码注释要求：
```
def run(self, transcripts, dialog_id):
        """
        @Description: 针对于单个topic做测试
        @Params: transcripts [{"speech": <string>, "target": <string>, "start_time": <string>, "end_time": <string>}]
        @Return:
            {
                "dialog_id": "1000",
                "matched": [
                    {
                        "score": 0.5454545454545454,
                        "source": "没有了",
                        "matched": "那我也没有办法了",
                        "start_time": "08:06:38",
                        "end_time": "08:06:43",
                        "origin": "没有了没有了"
                    }
                ],
            }
        """
```
