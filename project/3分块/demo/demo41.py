import re

text = "这是一个示例文本。\n这是第二行。\n这是第三行。"

# 使用正则表达式迭代找到所有换行符的位置
iter_matches = re.finditer(r'\n', text)

# 获取第一个和第二个换行符的位置
first_newline_pos = None
second_newline_pos = None

count = 0
for match in iter_matches:
    if count == 0:
        first_newline_pos = match.start()
    elif count == 1:
        second_newline_pos = match.start()
        break  # 只需要前两个换行符的位置
    count += 1

# 输出第一个和第二个换行符的位置
print("第一个换行符出现在位置:", first_newline_pos)
print("第二个换行符出现在位置:", second_newline_pos)