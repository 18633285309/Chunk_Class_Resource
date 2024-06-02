import re


def merge_three_sentences(text, keyword):
    # 分割文本为句子列表
    sentences = text.split('。')

    # 检查是否有连续三句以关键字开头
    count = 0
    start_index = -1
    for i, sentence in enumerate(sentences):
        if sentence.strip().startswith(keyword):
            count += 1
            if count == 1:
                start_index = i
            elif count == 3:
                # 合并三句话
                block_a = ' '.join(sentences[start_index:i + 1])
                # 获取块A前面的内容和块A后面的内容
                block_before = ' '.join(sentences[:start_index])
                block_after = ' '.join(sentences[i + 1:])
                return [block_before, block_a, block_after]
        else:
            count = 0

    # 如果没有找到连续三句以关键字开头的句子，返回原文
    return [text]


# 示例使用
text = "据/观点倾向于有用和（或）有效，应用这些操作或治疗是合理的；Ⅱb类指有关证据/观点尚不能被充分证明有用和（或）有效，可考虑应用。Ⅲ类：已证实和（或）一致公认无用和（或）无效，并对一些病例可能有害的操作或治疗，不推荐使用。对证据水平表达如下。证据水平A：资料来源于多项随机临床试验或荟萃分析。证据水平 B：资料来源于单项随机临床试验或多项非随机对照研究。证据水平 C：仅为专家共识意见和（或）小型临床试验、回顾性研究或注册登记研究。心衰概述心衰是多种原因导致心脏结构和（或）功能的异常改变，使心室收缩和（或）舒张功能发生障碍，从而引起的一组复杂临床综合征，主要表现为呼吸困难、疲乏和液体潴留（肺淤血、体循环淤血及外周水肿）等。"
keyword = "证据水平"
result = merge_three_sentences(text, keyword)
print(result)
