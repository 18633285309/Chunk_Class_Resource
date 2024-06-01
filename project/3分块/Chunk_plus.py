
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

        '''
        :param pages_text_list:
        :return:
        '''
        def asist(handle_text,target_index1,finaly_len):
            def text_find_to_max_size(text_find):
                res_split = text_find.split('。')
                print(len(res_split))
                return res_split
            flag = False
            if finaly_len != self.max_size:
                flag = True
            '''
            :param handle_text:
            :param target_index1:
            :param finaly_len:
            :return:
            '''
            #空列表
            items = []
            if target_index1 <= 5:
                # 找文本
                text_pre = text_find_to_max_size(handle_text)
                # 构造
                for items_list in text_pre:
                    items_list = items_list.replace('\n','')
                    item = {'content': items_list, 'ok_split': True}
                    # 添加
                    items.append(item)
                return items
            else:
                # 找文本
                text_pre = handle_text[:target_index1]
                # 构造
                item = {'content': text_pre, 'ok_split': False}
                # 添加
                items.append(item)
                if finaly_len is None:
                    # 找文本
                    text_later = handle_text[target_index1:]
                    res = text_find_to_max_size(text_later)
                    for item_list in res:
                        # 构造
                        item_list = item_list.replace('\n','')
                        item = {'content': item_list, 'ok_split': True}
                        # 添加
                        items.append(item)
                    # 返回
                    return items
                else:
                    # 找文本
                    text_find = handle_text[target_index1:target_index1 + finaly_len]
                    if len(text_find) > self.max_size:
                        text_finds = text_find_to_max_size(text_find)
                    else:
                        text_finds = [text_find]

                    for item in text_finds:
                        # 构造

                        item_find = {'content': item.replace('\n', ''), 'ok_split': True}

                        # 添加

                        items.append(item_find)

                    # 找文本
                    text_later = handle_text[target_index1 + finaly_len:]
                    # 构造
                    item = {'content': text_later, 'ok_split': False}
                    # 添加
                    items.append(item)
                    # 返回
                    return items
        #存储每一页列表
        page_num = []
        #存储所有页列表
        all_page_num = []
        is_other = False
        set_len = 5
        if len(pages_text_list)>=set_len:
            pages_text_list_split = pages_text_list[:set_len]
            is_other = True
        else:
            pages_text_list_split = pages_text_list
        # 前5页内容
        for handle_text in pages_text_list_split:

            #导包
            import re
            #匹配摘要
            match_ab = re.search(r'摘要|摘\s+要', handle_text)

            #不为空
            if match_ab:
                # 摘要位置
                target_index1 = match_ab.start()
                if target_index1 == 0:
                    pre=  False
                #匹配关键字
                match_key = re.search(r'关键词|关\s+键\s+词', handle_text)
                #找到
                if match_key:
                    # 关键字位置
                    match_key_index1 = match_key.start()

                    text = handle_text[match_key_index1:]

                    # 使用正则表达式搜索第一个换行符
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
                    if first_newline_pos is None :
                        items = asist(handle_text, target_index1, None)
                        # 添加第一页
                        all_page_num.append(items)
                    else:
                        line_key = first_newline_pos
                        if line_key <=5 :
                            if second_newline_pos is not None:
                                line_key = second_newline_pos
                                # 长度
                                finaly_len = match_key_index1 - target_index1 + line_key
                                # 进入函数
                                items = asist(handle_text, target_index1, finaly_len)

                                # 添加第一页
                                all_page_num.append(items)
                            else:
                                # 进入函数
                                items = asist(handle_text, target_index1, None)
                                # 添加第一页
                                all_page_num.append(items)
                        else:
                            finaly_len = match_key_index1 - target_index1 + line_key
                            # 进入函数
                            items = asist(handle_text, target_index1, finaly_len)

                            # 添加第一页
                            all_page_num.append(items)
                else:

                    #进入函数
                    items = asist(handle_text,target_index1,None)
                    #添加第一页
                    all_page_num.append(items)


            else:
                #直接存储
                item = {'content': handle_text, 'ok_split': False}
                #添加
                page_num.append(item)
                #添加第一页
                all_page_num.append(page_num)


        if is_other:
            for handle_text in pages_text_list[set_len:]:
                # 直接存储
                item = {'content': handle_text, 'ok_split': False}
                # 添加
                page_num.append(item)
                # 添加第一页
                all_page_num.append(page_num)

        '''
        测试
        '''
        for j,item in enumerate(all_page_num[:set_len]):
            for len_item in item:
                print(len_item)
                print('len(i[content])',len(len_item['content']))
                print('一页几个chunk',len(item))
                print('page',j)
                print('*******************************************************************************************************************************************')
            print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')




        #返回结果
        return all_page_num

    '''
    输入类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
    返回类型[[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]，[{'content':'','ok_split':True or False}......]......]
        '''
    #合并标题下的（\d+）
    def merge_child_title(self,pages_text_list):

        return []

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
        pass



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
        return res2
        res3 = self.child_title(res2)

        res4 = self.big_tile(res3)

        res5 = self.num_split(res4)

        res6 = self.same_prefix(res5)





'''
每一个函数的类型应该是接入类型[[{'content':'','ok_split':True or False}]]
    '''

if __name__ == '__main__':

    my_chunk_08 = My_Chunk_08A(max_size=150)

    from read_one_pdf import read_one_pdf
    from langchain_community.document_loaders import PyPDFLoader
    # 加载PDF文件
    # file_path = r'D:\桌面\chun_github1\project\data_pdf\cancer.pdf'
    loader = PyPDFLoader(r"D:\桌面\chun_github1\project\data_pdf\rag_test.pdf")
    datas = loader.load_and_split()
    # print(data)
    # data = datas[0]
    # print(data)

    # pages_text_list = read_one_pdf(file_path)
    pages_text_list = [data.page_content for data in datas]
    # print(pages_text_list[0])
    res = my_chunk_08.main(pages_text_list)

    print(res)