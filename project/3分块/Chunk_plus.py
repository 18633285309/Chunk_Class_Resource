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
        result = []  # 存储最终的分割结果

        for text_list in pages_text_list:
            chunks = []  # 存储每个文本块的分割结果
            for item in text_list:
                text = item['content']
                ok_split = item['ok_split']

                if not ok_split:
                    # 如果不需要分割，直接添加到chunks
                    chunks.append({'content': text, 'ok_split': False})
                    continue

                lines = text.split('\n')
                i = 0

                while i < len(lines):
                    # Handle section headers
                    if re.match(r'^(第[一二三四五六七八九十]\节)', lines[i]):
                        header = lines[i]
                        content = []
                        i += 1

                        while i < len(lines) and not re.match(r'^(第[一二三四五六七八九十]\节)', lines[i]):
                            if re.match(r'^([1-9]\.?)', lines[i]):
                                subheader = lines[i]
                                subcontent = []
                                i += 1

                                while i < len(lines) and not re.match(r'^([1-9]\.?)', lines[i]) and not re.match(
                                        r'^(第[一二三四五六七八九十]\节)', lines[i]):
                                    subcontent.append(lines[i])
                                    i += 1

                                if len(subcontent) > 0:
                                    chunks.append(
                                        {'content': subheader + '\n' + '\n'.join(subcontent), 'ok_split': True})
                            else:
                                content.append(lines[i])
                                i += 1

                        if len(content) > 0:
                            chunks.append({'content': header + '\n' + '\n'.join(content), 'ok_split': True})

                    # Handle other sections
                    elif re.match(r'^([a-zA-Z]+)\s+[-=]{3,}', lines[i]) or re.match(r'^附', lines[i]):
                        header = lines[i]
                        content = []
                        i += 1

                        while i < len(lines) and not re.match(r'^([a-zA-Z]+)\s+[-=]{3,}', lines[i]) and not re.match(
                                r'^附', lines[
                                    i]) and not re.match(r'^(第[一二三四五六七八九十]\节)', lines[i]):
                            content.append(lines[i])
                            i += 1

                        if len(content) > 0:
                            chunks.append({'content': header + '\n' + '\n'.join(content), 'ok_split': True})

                    # Handle single lines
                    else:
                        chunks.append({'content': lines[i], 'ok_split': False})
                        i += 1

            result.append(chunks)

        return result

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

    file_path = 'your_pdf_path'

    pages_text_list = read_one_pdf(file_path)

    res = my_chunk_08.main(pages_text_list)

    print(res)