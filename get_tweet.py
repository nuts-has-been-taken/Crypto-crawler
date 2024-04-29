from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
from login import login
import time

def get_tweets(username):
    # 使用Selenium開啟Chrome瀏覽器
    driver = webdriver.Chrome()

    # 登入
    login(driver)

    # 獲取用戶的Twitter頁面
    base_url = f"https://twitter.com/{username}"
    driver.get(base_url)
    time.sleep(7)

    for _ in range(3):
        driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    with open(f'./{username}.json', 'w', encoding='utf-8') as json_file:
        json_file.write("[\n")

    last_row_time = []
    current_row_time = []

    while True:
        # 獲取頁面的HTML內容
        html = driver.page_source

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, "html.parser")

        # 獲取貼文
        tweets = soup.find_all("div", class_="css-175oi2r r-eqz5dr r-16y2uox r-1wbh5a2")
        records = []
        for tweet in tweets:
            record = {}
            time_element = tweet.find("time")
            if time_element == None:
                datetime_value = None
            else:
                datetime_value = time_element['datetime']
            if datetime_value not in last_row_time:
                tweet_text = tweet.find("div", class_="css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim")
                repost_text = tweet.find("div", class_="css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim r-14gqq1x")
                if tweet_text or repost_text:
                    #print('--------------推文-----------------')
                    record['time'] = datetime_value
                    #print(f'時間 : {datetime_value}')
                    if tweet_text:
                        record['tweet_text'] = tweet_text.get_text()
                        #print(f'內容 : {tweet_text.get_text()}')
                    if repost_text:
                        record['repost_text'] = repost_text.get_text()
                        #print(f'轉推 : {repost_text.get_text()}')
                    #print('-----------------------------------')
                    records.append(record)
                    current_row_time.append(datetime_value)
        # 清空時間
        if current_row_time == []:
            print('---------爬文結束---------')
            break
        last_row_time = current_row_time.copy()
        current_row_time.clear()
        # 紀錄
        write_to_json(records, username)
        # 往下滑
        for _ in range(6):
            driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    # 關閉瀏覽器
    driver.quit()

    # 補齊
    new_data = ""
    with open(f'./{username}.json', 'r', encoding='utf-8') as json_file:
        lines = json_file.readlines()
        last_line = lines[-1].strip()
        if last_line == '},':
            json_file.seek(0)
            new_data = json_file.read()[:-2]
    with open(f'./{username}.json', 'w', encoding='utf-8') as json_file:
        json_file.write(new_data)
        json_file.write("\n]")
    return 

def write_to_json(records:list, user:str):
    with open(f'./{user}.json', 'a', encoding='utf-8') as json_file:
        for record in records:
            json.dump(record, json_file, ensure_ascii=False, indent=4)
            json_file.write(',\n')
    return

if __name__ == "__main__":
    username = "VitalikButerin"
    elon_tweets = get_tweets(username)
