import requests
from bs4 import BeautifulSoup
import re
import os
from ThreadPool import ThreadPool
from functools import partial
from tqdm import tqdm
from selenium import webdriver
import redis


redis_pool = redis.ConnectionPool(host='0.0.0.0', port=6379, decode_responses=True)
# pool = redis.ConnectionPool(host=conf.REDIS_IP, port=6379, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)
name_url = {}

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
    'User-Agent': user_agent[2],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
    'Host': 'v26.douyinvod.com'
}

down_HEADER = {
    'User-Agent': user_agent[0],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
    # 'Host': 'v26.douyinvod.com'

}

option = webdriver.ChromeOptions()
option.add_argument('--headless')
# driver = webdriver.Chrome(options=option)
# driver = webdriver.Chrome()#
from concurrent.futures import ThreadPoolExecutor
import json

pool = ThreadPoolExecutor(8)



element_class = {"user_logo": 'CjPRy13J',"video_list": 'ECMy_Zdt'}


# print(cookie)
request_data = {
    "operationName": "visionProfilePhotoList",
    "variables": {
        "userId": "3xmrk3e8i8magw6",
        "pcursor": "",
        "page": "detail",
        "webPageArea": "profilexxnull"
    },
    "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"
}


# print("初始化爬虫")
save_path_prefix = './Downloads/douyin'


def up_is_exist(name):
    folder = os.path.exists(os.path.join(save_path_prefix, name))
    if not folder:
        return False
    return True


def download(url, dirname, file_name='a.mp4', prefix=save_path_prefix):
    # print(url, dirname, file_name, prefix)
    r = requests.get(url, down_HEADER)
    if r.status_code == 200:
        path = os.path.join('', prefix, dirname)
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        # print("下载 "+ url)
        with open(os.path.join('', prefix, dirname, file_name.replace(' ', '')), "wb") as code:
            code.write(r.content)
        #         code = '200'
        return "200"
    else:
        print('\n http error : ', r.status_code)
        #         code = '404'
        return "404"


def getHTMLText(url):
    r = requests.get(url, get_HEADER)
    #     print("status_code: ", r.status_code)
    #         r.raise_for_status()
    #         r.encoding = r.apparent_encoding
    r.encoding = "utf-8"
    return r.text, r.status_code


import json
def down_one_video(download_list):
# def down_one_video(url, name, index):

    _option = webdriver.ChromeOptions()
    # _option.add_argument('--headless')
    # _option.add_argument('--headless')
    _driver = webdriver.Chrome()
    retry_times = 0

    with tqdm(total=len(download_list)) as t:
        for index,urls in enumerate(download_list):
            url = urls[0]
            name = urls[1]
            t.set_postfix(w=url)
            t.update(1)
            t.set_description(name)
            # tqdm.set_description_str(name)

            try:
                # html, code = getHTMLText(url)
                # html = driver.get(url)

                def find_vedio_url(url):
                    _driver.get(url)
                    html = _driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    # video = soup.find(name='video',attrs={'class':'mtz-vlc-klfbf'})
                    title = soup.find(name='title').text
                    # print(html)
                    import re
                    res = re.findall(r"v3-web.douyinvod.com(.+?)%2F%3F", html)
                    return res,title
                base_url = 'https://v26.douyinvod.com{}'
                base_url = 'https://v3-web.douyinvod.com{}'
                prefix = 'v3-web.douyinvod.com'
                res,title= find_vedio_url(url)
                if res == None or len(res)==0:
                    # print("没有检索到视频url,开始重试",url)
                    # return
                    t.set_description("没有检索到视频url,开始重试"+url)
                    while True:
                        res,title = find_vedio_url(url)
                        retry_times += 1
                        if retry_times > 2:
                            break
                        elif res != None or len(res)>0:
                            break
                if retry_times > 2 and len(res)==0:
                    continue
                retry_times  = 0
                res = res[0]
                res = str(res).replace('%2F', '/')
                # print('download ', title, base_url.format(res) + '/')
                download(base_url.format(res) + '/', name, file_name='{}.mp4'.format(title))
                redis_client.hset('in', name,
                              str(round((index + 1) / len(download_list),  2) * 100) + '##' + " [{}/{}]".format(index+1, len(download_list)))
            except Exception as e:
                # print(e)
                print('down_one_video ERROR', e, url)
                pass
    _driver.quit()




def down(lis, name, progress=True):
    if progress:
        redis_client.hdel('pending', name_url[name])
    # redis_client.hset('fi', name, " [{}/{}]".format(index, len(lis)))
    download_list =[]
    for index, li in enumerate(lis):
        try:
            a = li.find(name='a')['href'][2:].replace("'",'')
            a = 'http://'+a
            # print(a)
            # print('download',a)
            # down_one_video(a, name, index)
            download_list.append((a,name))
            # if progress:
            #     redis_client.hset('in', name,
            #                   str(round((index + 1) / len(lis),  2) * 100) + '##' + " [{}/{}]".format(index+1, len(lis)))
        except Exception as e:
            print('down ERROR', e)
            pass
    # print(download_list)
    down_one_video(download_list)

    if progress:
        redis_client.hset('fi', name, " [{}/{}]".format(index+1, len(lis)))
        redis_client.hdel('in', name)


def down_one_user(url, shared_url='', progress=False):
    global name_url
    # option.add_argument('--headless')
    # driver = webdriver.Chrome(options=option)
    _driver = webdriver.Chrome()
    # 删除原来的cookie
    _driver.delete_all_cookies()
    # driver.maximize_window()
    # 携带cookie打开
    # print(dy_cookies)
    # driver.get(url)
    # for key, value in dy_cookies.items():
    #     driver.add_cookie({'name':key,'value':value})

    # global driver
    print(url)
    if '##end##' in url:
        print('-' * 20, ' download finished ', '-' * 20)
        _driver.quit()
        return

    import time
    count = 0
    num_of_video = 0
    times = 0
    _driver.get(url)
    name = ''
    _lis = None
    _up_is_exist = False
    while True:
        html = _driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(name='title')
        # print(description['content'].split('：')[0])
        import string, random
        ba = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        name = title.text.split('的个人主页')[0]
        name_url[str(name)] = str(shared_url)
        if up_is_exist(name):
            _up_is_exist = True
            break
        if count == 0:
            print(name)
        count += 1
        lis = soup.findAll(name='li', attrs={"class": element_class['video_list']})
        # print(li)
        _lis = lis
        for li in lis:
            a = li.find(name='a')
            # print(a['href'])
        print('=' * 15, '>', name, ' len:', len(lis))
        if len(lis) == num_of_video:
            times += 1
        if len(lis) == num_of_video and times > 2:
            print("所有视频检索完毕", name, len(lis))
            # down(lis,name)
            break

        # if len(lis) >30:
        #     # print("所有视频检索完毕", name, len(lis))
        #     # down(lis,name)
        #     break

        num_of_video = len(lis)
        # e0fe394964bbd9fef7d310c80353afdd - scss
        # print(html)
        js = "var q=document.documentElement.scrollTop=100000"
        for i in range(0, 5):
            _driver.execute_script(js)
            time.sleep(1)
        time.sleep(1)
    if _up_is_exist:
        print(name, ' 已存在')
        if progress:
            redis_client.hdel('pending', name_url[name])
            redis_client.hset('fi', name, '已存在')
    else:
        print("所有视频检索完毕", name, len(lis))
        # print(lis)
        pool.submit(down, lis, name)
    # down(lis, name)
    _driver.quit()


def down_list():
    # global driver
    # driver = webdriver.Chrome()
    # option.add_argument('--headless')
    # driver = webdriver.Chrome(options=option)
    for url in open("douyin_urls.txt"):
        down_one_user(url)
    # driver.quit()

def down_by_search(key_word, filename):
    # global driver
    # option.add_argument('--headless')
    # driver = webdriver.Chrome(options=option)
    urls = []
    for url in open(filename):
        urls.append(url)
    for index, url in enumerate(tqdm(urls)):
        down_one_video(url, key_word, index)
    # driver.quit()


import time


def down_by_keyword(key_word, filename):
    global driver
    driver = webdriver.Chrome()
    # a3cc5072a10a34f3d46c4e722ef788c1 - scss
    base = 'https://www.douyin.com/search/{}?publish_time=0&sort_type=1&source=normal_search&type=video'
    # base = 'https://www.douyin.com/search/%E5%A4%A7%E9%95%BF%E8%85%BF?publish_time=0&sort_type=0&source=normal_search&type=video'
    driver.get(base.format(key_word))
    js = "var q=document.documentElement.scrollTop=100000"
    time.sleep(20)
    for i in range(0, 100):
        driver.execute_script(js)
        time.sleep(0.5)
    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    # users = soup.findAll(name='li',attrs={"class":'be642325476cd60928ab49ab10619761-scss'})
    users = soup.findAll(name='li', attrs={"class": 'a3cc5072a10a34f3d46c4e722ef788c1-scss'})
    print(len(users))
    users_url = []
    for user in users:
        # print(user)
        # url = user.find(name='a',attrs='caa4fd3df2607e91340989a2e41628d8-scss cfe2ef83d29eb6b3f56d991142d5e56e-scss _05b3a1a1aef60a7f51ee7a015550c6b4-scss')
        url = user.find(name='a')
        print(url['href'])
        users_url.append(url['href'])
        print('-' * 60)
        # print(user)
        # print('-'*60)
    # for user in users_url:
    with open(filename, 'a+') as f:
        for user in users_url:
            f.write(str(user) + '\n')  # 加\n换行显示
    driver.quit()


def _down_by_keyword():
    for key_word in ['弹力摇']:
        url_file_name = key_word + '.txt'
        down_by_keyword(key_word, url_file_name)
        # down_list()
        down_by_search(key_word, url_file_name)
    driver.quit()
    pool.stop()



def douyin_new_web(url='https://www.douyin.com/user/MS4wLjABAAAAwA8MOMMTmHkOZmX1WnF3xhd5Eq0wxOtbincMXrDD8hU'):
    html,code = getHTMLText(url)
    print(html)
    # vfBNMCpa
    soup = BeautifulSoup(html, 'html.parser')
    # users = soup.findAll(name='li',attrs={"class":'be642325476cd60928ab49ab10619761-scss'})
    video_list = soup.findAll(name='div', attrs={"class": 'vfBNMCpa'})
    print(video_list)

def down_up_by_appshare(url):
    # global driver
    print('开始下载 ', url)
    try:
        # html, code = getHTMLText(url)
        # html = driver.get(url)
        # time.sleep(10)
        _driver = webdriver.Chrome()
        _driver.get(url)
        html = _driver.page_source
        # html = driver.get(url)
        # html = driver.get(url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(name='title').text
        print('-'*100)
        # print(html)
        print('-'*100)
        import re
        base_url = 'https://v3-web.douyinvod.com{}'

        # res = re.findall(r"v3-web.douyinvod.com(.+?)%2F%3F", html)[0]
        up_div = soup.find(name='div', attrs={'class': element_class['user_logo']})
        up_url = up_div.find(name='a')
        print('up 主页url: ', up_url['href'])
        # res = str(res).replace('%2F', '/')
        # print('download ', title, base_url.format(res) + '/')
        down_one_user('https://'+up_url['href'][2:], url)
        # download(base_url.format(res) + '/', name, file_name='{}.mp4'.format(title))
    except Exception as e:
        print('ERROR', e)
        pass
    _driver.quit()


# down_list()
