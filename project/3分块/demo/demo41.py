import re

def split_text_into_blocks(text):
    """
    Split the given text into blocks based on titles and sentences.

    Args:
    text (str): The input text to be split.

    Returns:
    list: A list of text blocks.
    """

    # 编译正则表达式，匹配以数字标题开始的行
    title_pattern = re.compile(r'^(\d+(\.\d+)*)\s+', re.MULTILINE)

    # 找到所有匹配项的起始索引
    title_matches = [m.start() for m in title_pattern.finditer(text)]

    # 将每个标题及其后面的文本分割成块
    blocks = []
    for i in range(len(title_matches)):
        start = title_matches[i]
        end = len(text) if i == len(title_matches) - 1 else title_matches[i+1]
        block = text[start:end].strip()
        blocks.append(block)

    # 检查最后一个块是否需要进一步分割
    sentence_pattern = re.compile(r'\.\s*\n')
    last_block_sentences = sentence_pattern.split(blocks[-1])
    if len(last_block_sentences) > 1:
        # 如果最后一个块包含多个句子，分割它们
        blocks[-1:] = [sentence.strip() for sentence in last_block_sentences if sentence.strip()]

    return blocks

# 示例文本
text = """
这是一段开头的语句。
2.1 医疗
这里描述了一些医疗相关的信息。
2.1.1 基础医疗
关于基础医疗的详细内容。
2.1.2 高级医疗
关于高级医疗的详细内容。
2.2 教育
教育方面的描述。
2.2.1 基础教育
基础教育相关的信息。
2.2.2 高级教育
关于高级教育的详细内容。
3.1 经济
经济的概述。
3.1.1 农业
农业相关的信息。
3.1.2 工业
工业相关的信息。
这里还有一些其他的文本。
"""

# 使用函数分割文本
blocks = split_text_into_blocks(text)

# 打印分块结果
for block in blocks:
    print(block)
    print("------")  # 分块之间的分隔线
