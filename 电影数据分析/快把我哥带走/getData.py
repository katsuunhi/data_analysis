'''import requests
import pandas as pd

base_url = "http://m.maoyan.com/mmdb/comments/movie/1203084.json?_v_=yes&offset="

#爬取每一页评论
def crawl_one_page_data(url):
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    #页面访问失败
    if response.status_code != 200:
        return []
    
    return response.json()

#解析每一个获得的结果
def parse(data):
    result = []
    #影评数据在 ctms这个key中
    comments = data.get("cmts")
    
    if not comments:
        return []
    
    for cm in comments:
        yield[cm.get("id"),#影评id
              cm.get("time"),#影评时间
              cm.get("score"),#影评得分
              cm.get("cityName"),#影评城市
              cm.get("nickName"),#影评人
              cm.get("gender"),#影评人性别，1表示男，2表示女
              cm.get("content")]#影评内容
             
#爬取影评
def crawl_film_review(total_page_num=100):
    data = []
    for i in range(1, total_page_num + 1):
        url = base_url + str(i)
        crawl_data = crawl_one_page_data(url)
        if crawl_data:
            data.extend(crawl_data)
        return data

columns = ["id","time", "score", "city", "nickname", "gender", "content"]
df = pd.DataFrame(crawl_film_review(100),columns=columns)
#将性别映射后的数字转为汉字
df["gender"] = np.where(df.gender == 1,"男性","女性")

#根据id去除重复影评
df = df.drop_duolicates(subset=["id"])

#保存抓取数据到本地
if __name__ == '__main__':
    df.to_csv("《一出好戏》影评_1000.csv",index=False)
    df = pd.read_csv("《一出好戏》影评_1000.csv",encoding="gbk")'''

import requests
import time 
import random
import json

#获取每一页数据
def get_one_page(url):

    response = requests.get(url=url)
    if response.status_code == 200:
        return response.text
    return None

#解析每一页数据
def parse_one_page(html):

    data = json.loads(html)['cmts']#获取评论内容
    for item in data:
        yield{
        'date':item['time'].split(' ')[0],
        'nickname':item['nickName'],
        'city':item['cityName'],
        'rate':item['score'],
        'conment':item['content']
        }

#保存到文本文档中
def save_to_txt():
    for i in range(1,101):

        print("开始保存第%d页" % i)
        url = 'http://m.maoyan.com/mmdb/comments/movie/1216446.json?_v_=yes&offset=' + str(i)

        html = get_one_page(url)
        for item in parse_one_page(html):
            with open('快把我哥带走.txt','a',encoding='utf-8') as f:
                f.write(item['date'] + ','+item['nickname'] +','+item['city'] +','
                    +str(item['rate']) +',' +item['conment']+'\n')
                #time.sleep(random.randint(1,100)/20)
                time.sleep(2)

#去重重复的评论内容
def delete_repeat(old,new):
    oldfile = open(old,'r',encoding='utf-8')
    newfile = open(new,'w',encoding='utf-8')
    content_list = oldfile.readlines() #获取所有评论数据集
    content_alread = [] #存储去重后的评论数据集

    for line in content_list:
        if line not in content_alread:
            newfile.write(line+'\n')
            content_alread.append(line)

if __name__ == '__main__':
    save_to_txt()
    delete_repeat(r'快把我哥带走_old.txt',r'快把我哥带走_new.txt')