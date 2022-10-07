# from selenium import webdriver
# from selenium.webdriver.chrome import service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# options = Options()
# options.add_argument("--no-sandbox") #bypass OS security model
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems

# s=Service('../../../../usr/bin/chromedriver')
# driver = webdriver.Chrome(options=options, service=s)
# driver.get('http://google.com/')
# myPageTitle = driver.title
# print(myPageTitle)
# driver.quit()

# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import argparse
import datetime
import time, os
import pandas as pd
import multiprocessing
import warnings
import re
import json
from selenium.webdriver.common.by import By

warnings.filterwarnings(action='ignore')

BASE_DIR = '../../../../usr/bin/'
DATA_DIR = 'crawl_data'

web = os.path.join(BASE_DIR, 'chromedriver')
_url = "https://news.naver.com/"


news_type_list = ['today_main_news', 'section_politics', 'section_economy', 'section_society','section_life','section_world','section_it']
def replace_all(text, dic):
    for j in dic.values():
        text = re.sub(j, ' ', text)
    return text

def preprocessing_div_contents(x):
    find_re = {
        "find_icon" : r"©[.]+",
        "find_reporter" : r"[가-힣]{2,4} ([가-힣])*기자",
        "find_email" : r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        "find_things" : r'\[.+?\]',
        "find_useless_bracket" : r"\( *\)",
        "find_n" : r'\n',
        "find_backslash" : r"\\",
        "find_spaces" : r"  +"
    }

    result = replace_all(x, find_re)    

    return result.strip()

def crawling(news_type):
    def get_news_info_df(news_type):
        title = driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[2]/h2').text
        date = driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div[1]/span').text
        p = re.compile(r'[0-9]+.[0-9]+.[0-9]+')
        if p.match(date) is None:
            date = driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span').text

        pre_contents = driver.find_element_by_xpath('//*[@id="dic_area"]').text
        contents = preprocessing_div_contents(pre_contents)
        image_url = get_poster_url()
        news_url = driver.current_url
        df = pd.DataFrame([news_type, title, date, pre_contents, contents, image_url, news_url]).T
        df.columns = ['news_type', 'title', 'date', 'all_contents', 'contents', 'image_url', 'news_url']
        return df

    def get_poster_url():
        # get the image source
        try:
                img = driver.find_element_by_xpath('//*[@id="img1"]')
                src = img.get_attribute('src')
        except:
                src = "https://newsimg.sedaily.com/2019/01/23/1VE5F3W5WP_18.png"
        return src

    data_list = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920x1080')
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome('../../../../usr/bin/chromedriver', options=options)

    # title = driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[2]/h2').text
    # print("title", title)
    
    _url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1='
    if news_type == 'today_main_news':
        try :
            print("try")
            t_url = _url + '100'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            print("except")
            pass
        print("before for")
        # for i in range(1,6):
        #     print("in for")
        #     try:
        #         print("for try")
        #         text1 = driver.find_element_by_xpath('//*[@id="_rankingList0"]/li['+str(i)+']/div/div/div/a[1]').text
        #         print("after text1")
        #         text2 = driver.find_element_by_xpath('//*[@class="section _officeTopRanking1087473"]').text
        #         print(text1, ", ", text2)
        #         driver.find_element_by_xpath('//*[@id="_rankingList0"]/li['+str(i)+']/div/div/div/a[1]').text 
        #         driver.implicitly_wait(2)
        #         print("data_list before", data_list)
        #         data_list.append(get_news_info_df(news_type))
        #         print("data_list", data_list)
        #         driver.back()
            # except:
            #     driver.get(t_url)
        for i in range(1,6):
            try:
                print("try in for")
                driver.find_element_by_xpath('//*[@id="_rankingList0"]/li['+str(i)+']/div/div/div/a[1]').click() 
                print("after driver find")
                driver.implicitly_wait(2)
                data_list.append(get_news_info_df(news_type))
                driver.back()
            except:
                driver.get(t_url)
    elif news_type == 'section_politics':
        try :
            t_url = _url + '100'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            pass
        for i in range(1,6):
            try:
                driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[1]/div['+str(i)+']/div[1]/ul/li[1]/div[2]/a').click() 
                driver.implicitly_wait(2)
                data_list.append(get_news_info_df(news_type))
                driver.back()
            except:
                try:
                    driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[1]/div['+str(i)+']/div[1]/ul/li[1]/div/a').click()
                    driver.implicitly_wait(2)
                    data_list.append(get_news_info_df(news_type))
                    driver.back()
            
                except:
                    driver.get(t_url)
            
    elif news_type == 'section_economy':
        try :
            t_url = _url + '101'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            pass
    elif news_type == 'section_society':
        try :
            t_url = _url + '102'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            pass
    elif news_type == 'section_life':
        try :
            t_url = _url + '103'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            pass
    elif news_type == 'section_world':
        try :
            t_url = _url + '104'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            pass
    elif news_type == 'section_it':
        try :
            t_url = _url + '105'
            driver.get(t_url)
            driver.implicitly_wait(2)
        except:
            pass
        for i in range(1,6):
            try:
                driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div/div['+str(i)+']/div[2]/ul/li[1]/div[2]/a').click() 
                driver.implicitly_wait(2)
                data_list.append(get_news_info_df(news_type))
                driver.back()
            except:
                try:
                    driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div/div['+str(i)+']/div[2]/ul/li[1]/div/a').click()
                    driver.implicitly_wait(2)
                    data_list.append(get_news_info_df(news_type))
                    driver.back()
                except:
                    driver.get(t_url)
            
    if news_type != 'section_politics' and news_type != 'section_it' and news_type != 'today_main_news':
        for i in range(1,6):
            try:
                driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[1]/div['+str(i)+']/div[2]/ul/li[1]/div[2]/a').click() 
                driver.implicitly_wait(2)
                data_list.append(get_news_info_df(news_type))
                driver.back()
            except:
                try:
                    driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[1]/div['+str(i)+']/div[2]/ul/li[1]/div/a').click()
                    driver.implicitly_wait(2)
                    data_list.append(get_news_info_df(news_type))
                    driver.back()
                except:
                    driver.get(t_url)
           
    driver.quit()
    return data_list

def main(args):
        num_cpu = multiprocessing.cpu_count() - 1
        start_time = datetime.datetime.now()
        print("Start Time :", start_time)

#         pool = multiprocessing.Pool(2)
#         result = pool.imap(crawling, news_type_list)

#         pool.close()
#         pool.join()
        result = []
        for t in news_type_list:
            result += crawling(t)
            print("result",result)

        end_time = datetime.datetime.now()
        print("end_time")
        all_data = pd.concat(result).reset_index(drop=True)
#         all_data = list(result)
#         all_data = pd.concat(all_data).reset_index(drop=True)

        all_data.to_csv(os.path.join(BASE_DIR, DATA_DIR, start_time.strftime("%Y%m%d-%H") + '.csv', ), encoding='utf-8' ,index=False)
        print("End Date :", end_time)
        print(start_time.strftime("%Y%m%d-%H") + ', ' + str(all_data.shape) + ', 크롤링을 완료했습니다.')

if __name__ == "__main__":
        PARSER = argparse.ArgumentParser()
        ARGS = PARSER.parse_args()
        main(ARGS)

# main()