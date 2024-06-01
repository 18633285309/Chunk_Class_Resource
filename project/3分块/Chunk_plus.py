import re
#分块类
class My_Chunk_08A():

    #初始化
    def __init__(self,max_size):
        self.max_size = max_size

    '''
    函数的输入类型应该是['','','']
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''


    #摘要，关键字放在一个分块
    def  Abstract_extract(self,pages_text_list):
        pass

    '''
    输入类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''
    #合并标题下的（\d+）
    def merge_child_title(self,pages_text_list):
        pass

    '''
     输入类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''
    #2.1  2.1.1
    def child_title(self,pages_text_list):
        pass

    '''
     输入类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''
    #特殊字眼第一节 第二节不合
    def  big_tile(self,pages_text_list):
        result = []  # 存储处理后的文本块，每个文本块包含文本内容和是否可以进一步分割的标志

        for text_list in pages_text_list:  # 遍历每个页面上的文本块列表
            chunks = []  # 存储当前页面文本块的处理结果
            for item in text_list:  # 遍历文本块列表中的每个文本项
                text = item['content']  # 获取文本内容
                ok_split = item['ok_split']  # 获取是否可以进一步分割的标志

                if not ok_split:  # 如果不需要进一步分割
                    # 将整个文本作为一个块添加到chunks列表中
                    chunks.append({'content': text, 'ok_split': False})
                    continue  # 跳过本次循环的剩余代码，继续处理下一个文本项

                lines = text.split('\n')  # 将文本按行分割成列表
                i = 0  # 初始化行索引

                while i < len(lines):  # 遍历文本中的每一行
                    # 检测章节标题（例如：第一节）
                    if re.match(r'^(第[一二三四五六七八九十]\节)', lines[i]):
                        header = lines[i]  # 保存当前行为章节标题
                        content = []  # 初始化章节内容列表
                        i += 1  # 移动到下一行

                        while i < len(lines) and not re.match(r'^(第[一二三四五六七八九十]\节)', lines[i]):
                            # 检测子标题（例如：1.）
                            if re.match(r'^([1-9]\.?)', lines[i]):
                                subheader = lines[i]  # 保存当前行为子标题
                                subcontent = []  # 初始化子内容列表
                                i += 1  # 移动到下一行

                                while i < len(lines) and not re.match(r'^([1-9]\.?)', lines[i]) and not re.match(
                                        r'^(第[一二三四五六七八九十]\节)', lines[i]):
                                    subcontent.append(lines[i])  # 添加子内容
                                    i += 1  # 移动到下一行

                                if len(subcontent) > 0:
                                    # 将子标题和内容作为一个块添加到chunks列表中
                                    chunks.append(
                                        {'content': subheader + '\n' + '\n'.join(subcontent), 'ok_split': True})
                            else:
                                content.append(lines[i])  # 添加章节内容
                                i += 1  # 移动到下一行

                        if len(content) > 0:
                            # 将章节标题和内容作为一个块添加到chunks列表中
                            chunks.append({'content': header + '\n' + '\n'.join(content), 'ok_split': True})

                    # 检测其他类型的标题（例如：Title - 或者 附）
                    elif re.match(r'^([a-zA-Z]+)\s+[-=]{3,}', lines[i]) or re.match(r'^附', lines[i]):
                        header = lines[i]  # 保存当前行为其他类型的标题
                        content = []  # 初始化内容列表
                        i += 1  # 移动到下一行

                        while i < len(lines) and not re.match(r'^([a-zA-Z]+)\s+[-=]{3,}', lines[i]) and not re.match(
                                r'^附', lines[
                                    i]) and not re.match(r'^(第[一二三四五六七八九十]\节)', lines[i]):
                            content.append(lines[i])  # 添加内容
                            i += 1  # 移动到下一行

                        if len(content) > 0:
                            # 将标题和内容作为一个块添加到chunks列表中
                            chunks.append({'content': header + '\n' + '\n'.join(content), 'ok_split': True})

                    # 处理单独的行
                    else:
                        # 将单独的行作为一个块添加到chunks列表中
                        chunks.append({'content': lines[i], 'ok_split': False})
                        i += 1  # 移动到下一行

            result.append(chunks)  # 将当前页面的处理结果添加到最终结果列表中

        return result  # 返回处理后的文本块列表

    '''
     输入类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''
    #数字为开头的切分
    def num_split(self,pages_text_list):
        pass


    '''
     输入类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''
    #段落前几个字或字符相同的合起来
    def same_prefix(self,pages_text_list):
        pass



    def main(self,pages_text_list):

        res1 = self.Abstract_extract(pages_text_list)

        res2 = self.merge_child_title(res1)

        res3 = self.child_title(res2)

        res4 = self.big_tile(res3)

        res5 = self.num_split(res4)

        res6 = self.same_prefix(res5)

        return res6



'''
每一个函数的类型应该是接入类型[[{'content':'','ok_split':True or False}]]
    '''

if __name__ == '__main__':

    my_chunk_08 = My_Chunk_08A(max_size=150)

    from read_one_pdf import read_one_pdf

    file_path = ''

    pages_text_list = read_one_pdf(file_path)

    res = my_chunk_08.main(pages_text_list)

    print(res)