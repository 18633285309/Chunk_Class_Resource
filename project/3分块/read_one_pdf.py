"""
@author:    aj
@time:  2024/5/30
"""
import re
from PyPDF2 import PdfReader


def read_one_pdf(file_path= r'D:\桌面\新_检索增强知识库\pdf读取\PDFS\rag_test.pdf'):
    reader = PdfReader(file_path)

    page_sum = []

    for page in reader.pages:
        page_text = page.extract_text()

        page_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s.,;!?()\[\]{}<>=\'"#$%^&*+_=\\\-|\\/@`~]', '', page_text)

        page_sum.append(page_text)

    return page_sum


if __name__ == '__main__':
    file_path = r'PDFS/rag_test.pdf'
    res = read_one_pdf(file_path)

    print(res)
    print(len(res))
