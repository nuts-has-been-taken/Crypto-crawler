from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time

def login(driver:webdriver.Chrome):

    load_dotenv()

    driver.get("https://twitter.com/login")

    time.sleep(5)

    # 找到輸入框
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="input[type='text']")
    username_input = None

    for input_element in inputs:
        class_names = input_element.get_attribute("class")
        if "r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7" in class_names:  # 這是你提供的 class 名稱，可能會有變化，請確保它是正確的
            username_input = input_element
            break

    if username_input:
        username_input.send_keys(os.getenv("EMAIL"))
    else:
        print("找不到用戶名輸入框")

    username_input.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        inputs = driver.find_elements(by=By.CSS_SELECTOR, value="input[type='text']")
        username_check_input = None
        for input_element in inputs:
            class_names = input_element.get_attribute("class")
            if "r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7" in class_names:  # 這是你提供的 class 名稱，可能會有變化，請確保它是正確的
                username_check_input = input_element
                break
        if username_input:
            username_check_input.send_keys(os.getenv("USER_NAME"))
        else:
            print("找不到用戶名確認輸入框")
        username_check_input.send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        print("沒有被檢查到登入狀況異常")

    pass_input = driver.find_element_by_name("password")
    pass_input.send_keys(os.getenv("PASSWORD"))
    pass_input.send_keys(Keys.RETURN)
    time.sleep(2)
    return