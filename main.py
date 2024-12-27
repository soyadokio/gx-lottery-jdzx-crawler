import csv
import os
import pandas as pd
import random
import requests
import time
from bs4 import BeautifulSoup
from typing import List
from article import Article

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

def fetch_article(total_pages: int):
    total_page_articles: List[Article] = []
    for i in range(total_pages):
        print(f'fetching data of page of {i + 1}/{total_pages} ...')
        if i > 0:
            # 随机延迟1到2秒
            time.sleep(random.uniform(1, 2))
        url = f'http://www.lottery.gx.cn/sylm_171188/jdzx/index_{i + 1}.html'
        response = requests.get(url, headers=headers)

        # 获取当前页面的所有文章
        curr_page_articles = get_articles_from_html(response.text)

        # 追加到全部页面文章列表的尾部
        total_page_articles.extend(curr_page_articles)

    # 按照日期倒序排序
    total_page_articles.sort(key=lambda article: article.date, reverse=True)
    return total_page_articles

def get_articles_from_html(html_text: str) -> List[Article]:
    # 通过集合暂存的方式去重（返回时转回列表类型）
    articles = set()

    bs = BeautifulSoup(html_text, 'html.parser')
    ele_ul = bs.find(id='pagelist')
    ele_a_list = ele_ul.find_all('a')
    for ele_a in ele_a_list:
        link = ele_a['href']

        ele_span_1 = ele_a.find(class_='one-line')
        title = ele_span_1.text.strip()
        # 移除特殊字符
        title = title.replace('\u200b', '').replace('\xa0', '')

        ele_span_2 = ele_a.find_all('span')[-1]
        date = ele_span_2.text.strip('() \n\t')

        article = Article(title, link, date)
        if article:
            articles.add(article)
    return list(articles)

def output_to_csv(articles: List[Article]):
    with open('output/gx_lottery_jdzx.csv', 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(('title', 'link', 'date'))
        csv_rows = [[article.title, article.link, article.date] for article in articles]
        csv_writer.writerows(csv_rows)

def output_to_excel(articles: List[Article]):
    # 将文章列表转换为 DataFrame
    df = pd.DataFrame([article.__dict__ for article in articles])

    output_file = 'output/gx_lottery_jdzx.xlsx'
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    total_pages = 20
    total_page_articles = fetch_article(total_pages)

    # 确保output目录存在
    os.makedirs('output', exist_ok=True)
    # 输出 CSV
    output_to_csv(total_page_articles)
    # 输出 Excel
    output_to_excel(total_page_articles)
