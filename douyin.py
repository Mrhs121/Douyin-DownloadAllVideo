import requests
from bs4 import BeautifulSoup
import re
import os
from ThreadPool import ThreadPool
from functools import partial




user_agent = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]

get_HEADER = {
    'User-Agent': user_agent[0],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
    'referer':'https://www.douyin.com/video/6980526971419725092?previous_page=app_code_link',
    'Host':'v26.douyinvod.com'

}

down_HEADER = {
    'User-Agent': user_agent[0],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
    'Host':'v26.douyinvod.com'

}

from selenium import webdriver
option = webdriver.ChromeOptions()
option.add_argument('--headless')
from tqdm import tqdm

driver = webdriver.Chrome(options=option)
pool = ThreadPool(max_workers=4)
pool.start()

# cookie = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}
def download(url, dirname,file_name='a.mp4'):
    r = requests.get(url,down_HEADER)
    if r.status_code == 200:
        folder = os.path.exists("./douyin/" + dirname)
        if not folder:
            os.makedirs("./douyin/" + dirname)
        # print("下载 "+ url)
        with open("./douyin/" + dirname + '/'+file_name, "wb") as code:
            code.write(r.content)
        #         code = '200'
        return "200"
    else:
        print('\n http error : ', r.status_code)
        #         code = '404'
        return "404"

def getHTMLText(url):
    r = requests.get(url,get_HEADER)
    #     print("status_code: ", r.status_code)
    #         r.raise_for_status()
    #         r.encoding = r.apparent_encoding
    r.encoding = "utf-8"
    return r.text, r.status_code


def down(lis,name):
    for index,li in enumerate(tqdm(lis,desc=name)):
        try:
            a = li.find(name='a')['href']
            #print('download',a)
            html,code = getHTMLText(a)
            # print(html)
            import re
            base_url = 'https://v26.douyinvod.com{}'
            res = re.findall(r"v26.douyinvod.com(.+?)%2F%3F",html)[0]
            res = str(res).replace('%2F','/')
            #print(base_url.format(res)+'/')
            download(base_url.format(res)+'/',name,file_name='{}.mp4'.format(index))
        except Exception as e:
            # print('ERROR',e)
            pass

for url in open("douyin_urls.txt"):
    print(url)
    if '##end##' in url:
        print('-'*20,' download finished ','-'*20)
        driver.quit()
        import sys
        sys.exit(0)

    import time
    count = 0
    num_of_video = 0
    times = 0
    driver.get(url)
    name = ''
    _lis = None
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(name='title')
            # print(description['content'].split('：')[0])
        import string,random
        ba = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        name = title.text.split('的个人主页')[0]
        if count == 0:
            print(name)
        count += 1
        lis = soup.findAll(name='li',attrs={"class":'e0fe394964bbd9fef7d310c80353afdd-scss'})
        # print(li)
        _lis = lis
        for li in lis:
            a = li.find(name='a')
            # print(a['href'])
        print('-'*30,' len:', len(lis))
        if len(lis) == num_of_video:
            times +=1
        if len(lis) == num_of_video and times>2:
            print("所有视频检索完毕",name,len(lis))
            #down(lis,name)
            break
        num_of_video = len(lis)
        # e0fe394964bbd9fef7d310c80353afdd - scss
        # print(html)
        js="var q=document.documentElement.scrollTop=100000"
        for i in range(0,5):
            driver.execute_script(js)
            time.sleep(0.5)
        time.sleep(1)
    print("所有视频检索完毕", name, len(lis))
    pool.submit(partial(down, lis, name))
    # down(lis, name)

driver.quit()
pool.stop()


