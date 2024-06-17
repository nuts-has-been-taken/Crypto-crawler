import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import json
import pytz
import time

def save_record(records:list, name:str):
    with open(f'./{name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(records, json_file, ensure_ascii=False, indent=4)
    return

def crypto_compare_crawler(base_url:str, save_name:str):

    # Direct use crypto compare sentiment model
    origin_url = base_url
    taipei_tz = pytz.timezone('Asia/Taipei')
    records = []
    time_limit = True
    while time_limit:
        bm_news = requests.get(base_url)
        news_list = bm_news.json()["Data"]
        if news_list == None:
            break
        for news in news_list:
            ts_id = news["PUBLISHED_ON"]
            dt_object = datetime.fromtimestamp(ts_id, pytz.utc)
            taipei_time = str(dt_object.astimezone(taipei_tz))[:-15]
            sentiment = news["SENTIMENT"]
            data = {
                "date":taipei_time
            }
            if taipei_time < '2021-08-30':
                time_limit=False
                break
            if sentiment == "NEUTRAL":
                data['label']="neutral"
            elif sentiment == "POSITIVE":
                data['label']="bullish"
            elif sentiment == "NEGATIVE":
                data['label']="bearish"
            print(data)
            records.append(data)
        base_url = f"{origin_url}&to_ts={ts_id}"
    save_record(records, save_name)
    print("done")

    return

CRYPTO_COMPARE_URL = "https://data-api.cryptocompare.com/news/v1/article/list?categories=BTC&sortOrder=latest&source_ids="

def bm_cc_crawler():
    base_url = f"{CRYPTO_COMPARE_URL}bitcoinmagazine"
    save_name = "bm_cc_label"
    crypto_compare_crawler(base_url, save_name)

def cd_cc_crawler():
    base_url = f"{CRYPTO_COMPARE_URL}coindesk"
    save_name = "cd_cc_label"
    crypto_compare_crawler(base_url, save_name)

def cc_cc_crawler():
    base_url = f"{CRYPTO_COMPARE_URL}cryptocompare"
    save_name = "cc_cc_label"
    crypto_compare_crawler(base_url, save_name)

def cp_cc_crawler():
    base_url = f"{CRYPTO_COMPARE_URL}cryptopotato"
    save_name = "cp_cc_label"
    crypto_compare_crawler(base_url, save_name)

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
    for page_number in range(1,651):
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
    for page_number in range(1,1251):
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

def amb_crawler():
    records = []
    for page_number in range(1,1676):
        # 解析頁面新聞列表
        base_url = f"https://ambcrypto.com/category/new-news/page/{page_number}/"
        pc_news = requests.get(base_url)
        soup = BeautifulSoup(pc_news.content, "html.parser")
        news_list = soup.find("ul", class_="home-posts infinite-content").find_all("li", class_="home-post infinite-post")
        for page in news_list:
            # 取得每篇文章 link
            href = page.find("a").get("href")
            origin_news = requests.get(href)
            soup = BeautifulSoup(origin_news.content, "html.parser")
            # 取得文章日期
            date_time = soup.find("time", class_="post-date updated")
            if date_time:
                date_time = date_time.get("datetime")
                date_format = "%Y-%m-%d"
                date_time = datetime.strptime(date_time, date_format)
                # 取得新聞內容
                contents = soup.find("div", class_= "single-post-main-middle")
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
        if page_number%50==0:
            print(f"process data: {page_number}")
    save_record(records, "amb")

    return

def cb_crawler():
    records = []
    for page_number in range(1,688):
        # 解析頁面新聞列表
        body = {
            "action": "cb_jx_posts_loadmore",
            "cb_nonce": "0897cb70cf",
            "query_vars": {
                "category_name": "bitcoin",
                "error": "",
                "m": "",
                "p": 0,
                "post_parent": "",
                "subpost": "",
                "subpost_id": "",
                "attachment": "",
                "attachment_id": 0,
                "name": "",
                "pagename": "",
                "page_id": 0,
                "second": "",
                "minute": "",
                "hour": "",
                "day": 0,
                "monthnum": 0,
                "year": 0,
                "w": 0,
                "tag": "",
                "cat": 87838,
                "tax_query": {
                "0": {
                    "taxonomy": "category",
                    "terms": [
                    59784,
                    78
                    ],
                    "operator": "NOT IN"
                },
                "relation": "AND"
                },
                "ignore_sticky_posts": False,
                "suppress_filters": False,
                "cache_results": True,
                "update_post_term_cache": True,
                "update_menu_item_cache": False,
                "lazy_load_term_meta": True,
                "update_post_meta_cache": True,
                "post_type": "",
                "posts_per_page": 8,
                "nopaging": False,
                "comments_per_page": "50",
                "no_found_rows": False,
                "order": "DESC"
            },
            "is_archive": 1,
            "page": page_number,
            "queried_object_id": 87838
            }
        base_url = f"https://cryptobriefing.com/wp-admin/admin-ajax.php"
        tb_news = requests.post(base_url, data=body)
        soup = BeautifulSoup(tb_news.json()['html'], "html.parser")
        news_list = soup.find_all("li", class_="main-news-item")
        for news in news_list:
            href = news.find("a")['href']
            origin_news = requests.get(href)
            soup = BeautifulSoup(origin_news.content, "html.parser")
            date_time = soup.find("time", class_="timeago")
            if date_time:
                date_time = date_time.get("datetime")
                format_str = "%Y-%m-%d"
                date_time = parser.parse(date_time).strftime(format_str)
                contents = soup.find("div", class_= "article-content-wrapper")
                if contents:
                    contents = contents.find_all("p")
                    content = ""
                    for text in contents:
                        content += text.get_text()
                    record = {
                        "time":date_time,
                        "content":content
                    }
                    records.append(record)
        if page_number%50==0:
            print(f"process data: {page_number}")
    save_record(records, "tb")

    return

def ut_crawler():
    records = []
    for page_number in range(1,112):
        # 解析頁面新聞列表
        base_url = f"https://u.today/views/ajax?_wrapper_format=drupal_ajax&view_name=taxonomy_term&view_display_id=page_1&view_args=2462&view_path=%2Ftaxonomy%2Fterm%2F2462&view_base_path=taxonomy%2Fterm%2F%25&view_dom_id=52c67bd16940233b50b68e1d3cd5d7c272940ee2f0f01e7a30a9c20f2caf3d1a&pager_element=0&page={page_number}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=cryptod&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=cryptod%2Fglobal-styling%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Csystem%2Fbase%2Cviews%2Fviews.module%2Cviews_infinite_scroll%2Fviews-infinite-scroll"
        ut_news = requests.get(base_url)
        soup = BeautifulSoup(ut_news.json()[1]['data'], "html.parser")
        news_list = soup.find_all("div", class_="news__item")
        for news in news_list:
            href = news.find("a", class_="news__item-body")['href']
            origin_news = requests.get(href)
            soup = BeautifulSoup(origin_news.content, "html.parser")
            date_time = soup.find_all("div", class_="humble article__short-humble")[1].text.strip()
            date_time = datetime.strptime(date_time, "%a, %d/%m/%Y - %H:%M").strftime("%Y-%m-%d")
            contents = soup.find("div", class_= "article__content")
            if contents:
                contents = contents.find_all("p")
                content = ""
                for text in contents:
                    content += text.get_text()
                record = {
                    "time":date_time,
                    "content":content
                }
                records.append(record)
        if page_number%50==0:
            print(f"process data: {page_number}")
    save_record(records, "ut")
    return

if __name__ == "__main__":
    ut_crawler()