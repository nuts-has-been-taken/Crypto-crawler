import requests
from bs4 import BeautifulSoup
import json

def pc_crawler():
    records=[]
    for page_number in range(1,61):
        # 解析頁面新聞列表
        base_url = f"https://portalcripto.com.br/zh-TW/ultimas-noticias/bitcoin/%E9%A0%81%E9%9D%A2/{page_number}/"
        pc_news = requests.get(base_url)
        soup = BeautifulSoup(pc_news.content, "html.parser")
        news_list = soup.find("div", class_="cs-posts-area__main cs-posts-area__archive cs-posts-area__grid cs-display-borders-between-posts cs-posts-area__withsidebar")
        news = news_list.find_all("article")
        for page in news:
            # 取得每篇文章 link
            href = page.find("a", class_="cs-entry__title-wrapper").get("href")
            # 取得文章日期
            date_time = page.find("div", class_="cs-meta-date").text.strip()
            origin_news = requests.get(href)
            # 取得文章內容
            soup = BeautifulSoup(origin_news.content, "html.parser")
            contents = soup.find("div", class_="entry-content").find_all("p")
            content = ""
            for text in contents:
                content += text.get_text()
            record = {
                "time":date_time,
                "content":content
            }
            records.append(record)

    with open(f'./pc.json', 'w', encoding='utf-8') as json_file:
        json.dump(records, json_file, ensure_ascii=False, indent=4)

    return

if __name__ == "__main__":
    pc_crawler()
