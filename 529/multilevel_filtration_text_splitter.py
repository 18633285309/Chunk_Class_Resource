"""
@author:    aj

This module does something.

@time:  2024/5/26
说明：
             通用乱码处理
             标题
             表格
             摘要
             页码
             分块
             meta数据
             多路召回

贡献者@一个橙子@破碎的坚强@归零。@Regan@有时@青颜@元气满满Q@栗子
@goodbye：欢迎联系作者
         看不懂代码，不建议用。
        看得懂，不是你的力量。
"""
import os
import re
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine
#
class Aj_cglxyz_Multilevel_partitioning():

    """
    这是一个chunk类。

    这个类用于多层次过滤和分割文本。
    分块功能：
        标题合并           完成
        表格合并           完成
        摘要合并           完成
        页码id            完成
        分块id            完成
        元数据             完成
    """

    #初始化
    def __init__(
            self,
            max_chunk_size,
            file_path
    ):
        self.max_chunk_size = max_chunk_size
        self.file_path = file_path
        self.titles = self.extract_title_from_first_page(self.file_path)
    def extract_title_from_first_page(self,pdf_path):

        pages = extract_pages(pdf_path)
        first_page = next(pages)

        title = []
        max_font_size = 0

        for i in range(2):
            for element in first_page:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if isinstance(text_line, LTTextLine):

                            for char in text_line:
                                if isinstance(char, LTChar):
                                    if char.size > max_font_size:
                                        max_font_size = char.size

            for element in first_page:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        if isinstance(text_line, LTTextLine):

                            for char in text_line:
                                if isinstance(char, LTChar):
                                    if char.size == max_font_size:
                                        title.append(text_line.get_text().strip())
        tmp = []
        for i in title:
            if i not in tmp:
                tmp.append(i)
        return ''.join(tmp)

    def Read_pdf_files(self):

        reader = PdfReader(self.file_path)

        page_sum = []

        for page_id, page in enumerate(reader.pages, start=1):

            page_text = page.extract_text()
            #标题 表格 摘要
            page_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s.,;!?()\[\]{}<>=\'"#$%^&*+_=\\\-|\\/@`~]', '', page_text)


            res_guize_pipline = self.guize_pipline(page_text)
            chunk_start = len(page_sum)+1
            res_page_object = self.page_object(page_id,res_guize_pipline,chunk_start)

            page_sum.extend(res_page_object)

        return page_sum


    def slit_text(self,texts):
        def split_text_into_chunks(text, chunk_size):
            return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        res = split_text_into_chunks(texts,chunk_size=self.max_chunk_size)
        return res

    def chunk_func(self,page_id,text,chun_start):

        text_spliter = self.slit_text(text)
        res = []
        for items in text_spliter:
            item = {
                'title':self.titles,
                'page_id':page_id,
                'chunk_id':chun_start,
                'chunk_content':items
            }
            chun_start += 1
            res.append(item)
        return res


    def page_object(self,page_id,res_guize_pipline,chunk_start):
        chunk_start = chunk_start
        res = []
        for each_page_content in res_guize_pipline:
            res_each = self.chunk_func(page_id,each_page_content['text'],chunk_start)
            res.extend(res_each)
            chunk_start = len(res) + 1
        return res
    #规则
    def guize_pipline(self, page_text):

        #标题
        res_biaoti =  self.biaoti(page_text)

        # #标题
        res_biaoge =  self.biaoge(res_biaoti)

        #标题
        res_zhaiyao =  self.zhaiyao(res_biaoge)

        return res_zhaiyao


    # 标题
    def biaoti(self,page_text):
        chunks = []
        lines = page_text.split('\n')
        chunk = ""
        i = 1
        for line in lines:
            if re.match(r'^\d+\..+', line):
                item = {'text': None, 'issplit': None}
                if chunk:
                    if i % 2 == 1:
                        item['text'] = chunk.strip()
                        item['issplit'] = False
                        chunks.append(item)
                    else:
                        item['text'] = chunk.strip()
                        item['issplit'] = True
                        chunks.append(item)
                chunk = line
                i += 1
            else:
                chunk += line + '\n'
        if chunk:
            item = {'text': None, 'issplit': None}
            item['text'] = chunk.strip()
            item['issplit'] = False
            chunks.append(item)

        return chunks


    # 表格
    def biaoge(self,chunks_biaoti_item):

        # 使用正则表达式匹配摘要到连续换行符
        pattern = r"表\d+ "
        for i,biaoti_item in enumerate(chunks_biaoti_item):
            if biaoti_item['issplit']:
                continue
            item_texts = biaoti_item['text']
            match = re.search(pattern, item_texts, re.DOTALL)
            if match:
                table_prefix = match.group(0).strip()
                pre_index_split = item_texts.find(table_prefix)
                last_index_split = item_texts.find(table_prefix)+self.max_chunk_size

                pre_item =  {'text': item_texts[:pre_index_split], 'issplit': False}
                chunks_biaoti_item.insert(i,pre_item)
                biaoti_item['text'] = item_texts[pre_index_split:last_index_split+1]
                biaoti_item['issplit'] = True
                last_item =  {'text': item_texts[last_index_split+1:], 'issplit': False}
                chunks_biaoti_item.insert(i+2,last_item)

        return chunks_biaoti_item

    # 标题
    def zhaiyao(self, chunks_table_item):

        # 使用正则表达式匹配摘要到连续换行符
        pattern = r"(摘 要\n[\s\S]*?)\n\n"
        for i,biaoti_item in enumerate(chunks_table_item):
            if biaoti_item['issplit']:
                continue
            item_texts = biaoti_item['text']
            match = re.search(pattern, item_texts, re.DOTALL)
            if match:
                abstracts = match.group(1).strip()
                pre_index_split = item_texts.find(abstracts)

                pre_item =  {'text': item_texts[:pre_index_split], 'issplit': False}
                chunks_table_item.insert(i, pre_item)
                biaoti_item['text'] = item_texts[pre_index_split:pre_index_split+self.max_chunk_size]
                biaoti_item['issplit'] = True
                break

        return chunks_table_item

    #主逻辑
    def main(self):

        return self.Read_pdf_files()


#测试用例
if __name__ == '__main__':

    #初始化
    aj_multilevel_filtration_text_splitter = Aj_cglxyz_Multilevel_partitioning(
        max_chunk_size = 250,
        file_path = r'rag_test.pdf'
    )

    #处理
    res = aj_multilevel_filtration_text_splitter.main()

    for chunk in res:
        text_without_newlines = chunk['chunk_content'].replace('\n', '')
        pattern = r'\(\.\.\.\/{5}\)|\(\<{2}\)|\(\.\.\.\)|\(\(\(\)'
        cleaned_text = re.sub(pattern, '', text_without_newlines)
        pattern = r'\s*\(.\s*\.\s*\)'
        chunk['chunk_content'] = re.sub(pattern, '', cleaned_text)

    for chunk in res:
        print(f"Page title: {chunk['title']}, \nPage ID: {chunk['page_id']}, \nChunk ID: {chunk['chunk_id']}, \nContext: \n{chunk['chunk_content']}")
        print(
            '--------------------------------------------------------------------------------------------------------------')


