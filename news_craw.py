import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def save_record(records:list, name:str):
    with open(f'./{name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(records, json_file, ensure_ascii=False, indent=4)
    return

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

    save_record(records, "pc")

    return

def bc_crawler():
    records=[]
    for page_number in range(1,21):
        # 解析頁面新聞列表
        base_url = f"https://blockcast.it/category/news/reports/page/{page_number}/"
        pc_news = requests.get(base_url)
        soup = BeautifulSoup(pc_news.content, "html.parser")
        news_list = soup.find("div", class_="jeg_posts jeg_load_more_flag")
        news = news_list.find_all("article")
        for page in news:
            # 取得每篇文章 link
            href = page.find("a").get("href")
            origin_news = requests.get(href)
            # 取得文章內容
            soup = BeautifulSoup(origin_news.content, "html.parser")
            # 取得文章日期
            date_time = soup.find("div", class_="jeg_meta_date").text.strip()
            contents = soup.find("div", class_="content-inner").find_all("p")[:-1]
            content = ""
            for text in contents:
                content += text.get_text()
            record = {
                "time":date_time,
                "content":content
            }
            records.append(record)

    save_record(records, "bc")

    return

def cd_crawler():
    records=[]
    for page_number in range(1,101):
        # 解析頁面新聞列表
        base_url = f"https://www.coindesk.com/tag/bitcoin/{page_number}/"
        pc_news = requests.get(base_url)
        soup = BeautifulSoup(pc_news.content, "html.parser")
        news_list = soup.find_all("div", class_="article-cardstyles__AcTitle-sc-q1x8lc-1 PUjAZ articleTextSection")
        for page in news_list:
            # 取得每篇文章 link
            news_link = page.find("h6", class_="typography__StyledTypography-sc-owin6q-0 bhrWMt")
            href = news_link.find("a").get("href")
            # 取得文章日期
            date_time = page.find("span", class_="typography__StyledTypography-sc-owin6q-0 iOUkmj").text
            date_format = "%b %d, %Y at %I:%M %p"
            date_time = datetime.strptime(date_time[:-4].replace(".", ""), date_format)
            origin_news = requests.get(f'https://www.coindesk.com/{href}')
            # 取得文章內容
            soup = BeautifulSoup(origin_news.content, "html.parser")
            contents = soup.find("div", class_="contentstyle__StyledWrapper-sc-g5cdrh-0 gkcZwU composer-content")
            content = ""
            if contents:
                for text in contents:
                    content += text.get_text()
                record = {
                    "time":str(date_time),
                    "content":content
                }
                records.append(record)

    save_record(records, "cd")

    return

def cs_crawler():
    records=[]
    for page_number in range(1,161):
        # 解析頁面新聞列表
        base_url = f"https://cryptoslate.com/news/page/{page_number}/"
        pc_news = requests.get(base_url)
        soup = BeautifulSoup(pc_news.content, "html.parser")
        news_list = soup.find("div", class_="list-feed slate").find_all("div", class_="list-post")
        for page in news_list:
            # 取得每篇文章 link
            href = page.find("a").get("href")
            origin_news = requests.get(href)
            soup = BeautifulSoup(origin_news.content, "html.parser")
            # 取得文章日期
            date_time = soup.find("div", class_="post-date")
            if date_time:
                date_time = date_time.text.strip()
                date_format = "%b %d, %Y at %I:%M %p"
                date_time = datetime.strptime(date_time[:-4].replace(".", ""), date_format)
                # 取得新聞內容
                contents = soup.find("article", class_= "full-article")
                if contents:
                    contents = contents.find_all("p")
                    content = ""
                    for text in contents:
                        content += text.get_text()
                    record = {
                        "time":str(date_time),
                        "content":content
                    }
                    records.append(record)

    save_record(records, "cs")

    return

if __name__ == "__main__":
    # pc_crawler()
    # bc_crawler()
    # cd_crawler()
    cs_crawler()