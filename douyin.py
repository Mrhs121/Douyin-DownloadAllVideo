# https://v26.douyinvod.com/39b6566bccad5e7f9a95678753d3c491/60e48c5b/video/tos/cn/tos-cn-ve-15/5406fbea2c884782af5dd0ee1869c097/?a=6383&br=1041&bt=1041&cd=0%7C0%7C0&ch=26&cr=0&cs=0&cv=1&dr=0&ds=6&er=&l=20210707000106010212022142112D7E72&lr=all&mime_type=video_mp4&net=0&pl=0&qs=0&rc=amt3ZDU6Zm12NjMzNGkzM0ApPGQ7OGU1OGQ5N2g1ODc1aWdqbTZmcjRfcWNgLS1kLS9zc2IuNF8wYGJhMGMxM2MuYTA6Yw%3D%3D&vl=&vr=


import requests
from bs4 import BeautifulSoup
import re
import os
from mv.ThreadPool import ThreadPool
from functools import partial
from tqdm import tqdm
from selenium import webdriver

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
    'referer': 'https://www.douyin.com/video/6980526971419725092?previous_page=app_code_link',
    'Host': 'v26.douyinvod.com'

}

down_HEADER = {
    'User-Agent': user_agent[0],  # 浏览器头部
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 客户端能够接收的内容类型
    'Accept-Language': 'en-US,en;q=0.5',  # 浏览器可接受的语言
    'Connection': 'keep-alive',  # 表示是否需要持久连接
    'Host': 'v26.douyinvod.com'

}



option = webdriver.ChromeOptions()
option.add_argument('--headless')
driver = webdriver.Chrome(options=option)

pool = ThreadPool(max_workers=4)
pool.start()
c = 'ttwid=1%7CLab6rIp6rI50hyjHppm7A_s1AY2DhpFNVWZPFOEnL9U%7C1625587169%7Cb064cbb69b13e0d48130e92f60104f1c39121537d9bb8ab496d7ec7746324c85; MONITOR_WEB_ID=86f518e8-2b14-4bfe-a17d-a363408ae7ea; s_v_web_id=verify_kqs8mx7c_UsY1l6c3_68Qq_4Gcc_8bte_5O95OiXNAUli; passport_csrf_token_default=b4f26304cff4a8c02f2bf691ed31b94d; passport_csrf_token=b4f26304cff4a8c02f2bf691ed31b94d; n_mh=3TAsyBQ9TIOReANIuNLrZaSwE0wXPy61SN4Ofti2r3g; sso_uid_tt=12dc0ae1f5143f6953a15b64234b33d8; sso_uid_tt_ss=12dc0ae1f5143f6953a15b64234b33d8; toutiao_sso_user=4273e1021bda992fcc8a8d656c2ee3a7; toutiao_sso_user_ss=4273e1021bda992fcc8a8d656c2ee3a7; odin_tt=7502bf01876c63fe2cec24eb194bb66cee9f9f091d2d9bd7cc7c0002500a89d8cde6ce2bd10557fcc224da126910d8c6; passport_auth_status_ss=bd6d57b65a6c31d468534cee3806aeff%2C; sid_guard=60557fd519c063f31d7f30967717a876%7C1625587252%7C5183998%7CSat%2C+04-Sep-2021+16%3A00%3A50+GMT; uid_tt=cbdb9df0e89134e7b90a8546c0f6a629; uid_tt_ss=cbdb9df0e89134e7b90a8546c0f6a629; sid_tt=60557fd519c063f31d7f30967717a876; sessionid=60557fd519c063f31d7f30967717a876; sessionid_ss=60557fd519c063f31d7f30967717a876; passport_auth_status=bd6d57b65a6c31d468534cee3806aeff%2C; csrf_session_id=e9d0f336d4444490baf556a38fd80165'
cookie = {i.split("=")[0]: i.split("=")[1] for i in c.split(";")}


def download(url, dirname, file_name='a.mp4'):
    r = requests.get(url, down_HEADER)
    if r.status_code == 200:
        folder = os.path.exists("/Volumes/t2-ssd/douyin/" + dirname)
        if not folder:
            os.makedirs("/Volumes/t2-ssd/douyin/" + dirname)
        # print("下载 "+ url)
        with open("/Volumes/t2-ssd/douyin/" + dirname + '/' + file_name, "wb") as code:
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


def down_one_video(url, name, index):
    try:
        html, code = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find(name='title').text
        # print(html)
        import re
        base_url = 'https://v26.douyinvod.com{}'
        res = re.findall(r"v26.douyinvod.com(.+?)%2F%3F", html)[0]
        res = str(res).replace('%2F', '/')
        print('download ', title, base_url.format(res) + '/')
        download(base_url.format(res) + '/', name, file_name='{}.mp4'.format(title))
    except Exception as e:
        # print('ERROR',e)
        pass


def down(lis, name):
    for index, li in enumerate(tqdm(lis, desc=name)):
        try:
            a = li.find(name='a')['href']
            # print('download',a)
            down_one_video(a, name, index)
        except Exception as e:
            # print('ERROR',e)
            pass


def down_oneuser(url):
    print(url)
    if '##end##' in url:
        print('-' * 20, ' download finished ', '-' * 20)
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
        import string, random
        ba = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        name = title.text.split('的个人主页')[0]
        if count == 0:
            print(name)
        count += 1
        lis = soup.findAll(name='li', attrs={"class": 'e0fe394964bbd9fef7d310c80353afdd-scss'})
        # print(li)
        _lis = lis
        for li in lis:
            a = li.find(name='a')
            # print(a['href'])
        print('-' * 30, ' len:', len(lis))
        if len(lis) == num_of_video:
            times += 1
        if len(lis) == num_of_video and times > 2:
            print("所有视频检索完毕", name, len(lis))
            # down(lis,name)
            break
        num_of_video = len(lis)
        # e0fe394964bbd9fef7d310c80353afdd - scss
        # print(html)
        js = "var q=document.documentElement.scrollTop=100000"
        for i in range(0, 5):
            driver.execute_script(js)
            time.sleep(1)
        time.sleep(1)
    print("所有视频检索完毕", name, len(lis))
    pool.submit(partial(down, lis, name))
    # down(lis, name)


def down_list():
    for url in open("douyin_user.txt"):
        down_oneuser(url)


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
    # driver = webdriver.Chrome()
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
    # driver.quit()


def _down_by_keyword():
    for key_word in ['海贼王','路飞','火影']:
        url_file_name = key_word + '.txt'
        down_by_keyword(key_word, url_file_name)
        # down_list()
        down_by_search(key_word, url_file_name)


_down_by_keyword()
# down_list()
driver.quit()
pool.stop()
