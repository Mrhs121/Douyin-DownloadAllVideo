# https://v26.douyinvod.com/39b6566bccad5e7f9a95678753d3c491/60e48c5b/video/tos/cn/tos-cn-ve-15/5406fbea2c884782af5dd0ee1869c097/?a=6383&br=1041&bt=1041&cd=0%7C0%7C0&ch=26&cr=0&cs=0&cv=1&dr=0&ds=6&er=&l=20210707000106010212022142112D7E72&lr=all&mime_type=video_mp4&net=0&pl=0&qs=0&rc=amt3ZDU6Zm12NjMzNGkzM0ApPGQ7OGU1OGQ5N2g1ODc1aWdqbTZmcjRfcWNgLS1kLS9zc2IuNF8wYGJhMGMxM2MuYTA6Yw%3D%3D&vl=&vr=


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

# pool.start()
c = 'ttwid=1%7CLab6rIp6rI50hyjHppm7A_s1AY2DhpFNVWZPFOEnL9U%7C1625587169%7Cb064cbb69b13e0d48130e92f60104f1c39121537d9bb8ab496d7ec7746324c85; MONITOR_WEB_ID=86f518e8-2b14-4bfe-a17d-a363408ae7ea; s_v_web_id=verify_kqs8mx7c_UsY1l6c3_68Qq_4Gcc_8bte_5O95OiXNAUli; passport_csrf_token_default=b4f26304cff4a8c02f2bf691ed31b94d; passport_csrf_token=b4f26304cff4a8c02f2bf691ed31b94d; n_mh=3TAsyBQ9TIOReANIuNLrZaSwE0wXPy61SN4Ofti2r3g; sso_uid_tt=12dc0ae1f5143f6953a15b64234b33d8; sso_uid_tt_ss=12dc0ae1f5143f6953a15b64234b33d8; toutiao_sso_user=4273e1021bda992fcc8a8d656c2ee3a7; toutiao_sso_user_ss=4273e1021bda992fcc8a8d656c2ee3a7; odin_tt=7502bf01876c63fe2cec24eb194bb66cee9f9f091d2d9bd7cc7c0002500a89d8cde6ce2bd10557fcc224da126910d8c6; passport_auth_status_ss=bd6d57b65a6c31d468534cee3806aeff%2C; sid_guard=60557fd519c063f31d7f30967717a876%7C1625587252%7C5183998%7CSat%2C+04-Sep-2021+16%3A00%3A50+GMT; uid_tt=cbdb9df0e89134e7b90a8546c0f6a629; uid_tt_ss=cbdb9df0e89134e7b90a8546c0f6a629; sid_tt=60557fd519c063f31d7f30967717a876; sessionid=60557fd519c063f31d7f30967717a876; sessionid_ss=60557fd519c063f31d7f30967717a876; passport_auth_status=bd6d57b65a6c31d468534cee3806aeff%2C; csrf_session_id=e9d0f336d4444490baf556a38fd80165'
kuaishou_c = '_did=web_252270252416EEFB; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_f5605457d8649e60c33ac47b6730058d; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABvoKhzoY5ZmCrW6ihg0lpl8GhEXUoXVIEL0N4H8KrTP3xfVlQF2NFVBR1ExtZYpQ-HT6XznR3zRuZEXY1BbGS-Zy0ebLZ9H_fUkoAxVUh63NMEFjcJR-Nyr-d9ERTqqwACZDI0bbnHSXlRmhV-KTT_6KN1RW6T_imdaUG74Q8iLgdp0t0t4IvamUUYMdavjr1L4ccBO4r-3qyCTl9pk0prBoStVKEb-xUGkLo9u0A7O3lj4AGIiBOUP5BnzTeX8Y4d3U-PU9UceJI1SuknN5pl7OHSqxaqigFMAE; kuaishou.server.web_ph=6f7352378417cac345cf921c93278bff27c8; didv=1625938562000'
kuaishou_c = '_did=web_252270252416EEFB; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_f5605457d8649e60c33ac47b6730058d; didv=1625938562000; _bl_uid=C7k06qsRyFR3zF8vOihj82hrp5IX; ktrace-context=1|MS43NjQ1ODM2OTgyODY2OTgyLjkxNzcxNzM0LjE2MjU5NDQzMjMzNDQuNjE5NDcw|MS43NjQ1ODM2OTgyODY2OTgyLjc1MjkzMjQ4LjE2MjU5NDQzMjMzNDQuNjE5NDcx|0|graphql-server|webservice|false|NA; userId=2135609138; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABKWC-C-VBYuMBGOjOAJgBHoPYYSktfnvqYPJO_MtUZQegIygL8qel1nqQAhaFo0F30daqEyKS-HYANavTdFfXDa9aavGIfIKOrT9ckgvV3rckQcjZM65n0Sgr_5R52Moz1kisYu2NtyTLi28p2MlXYxBzuS7wrCLrox9Rk6KQ7OcqOBhVF6XADwz9LG6Hxz7R8uMwdu4-eJsDm7_wLMBHCxoSzFZBnBL4suA5hQVn0dPKLsMxIiBYaLg_l8wjkRBRq8_oK0xj-sakg4yYTVseRw9XGG4vyygFMAE; kuaishou.server.web_ph=c64fe76932c2f2f83423baa7effadb467c43'

dy_cookies = 'ttwid=1%7CZXz68xxvoU4R5QaRJNcnvwRuch5YAscF5EzxR601AEs%7C1627628360%7C931f090779804c4b660f4fe3b1cb6df0bd1470fa1a1108d7c29c6402c789e13f; MONITOR_WEB_ID=660b6b75-0e89-48dc-bc93-846eecc287a1'
dy_cookies = 'ttwid=1%7CZXz68xxvoU4R5QaRJNcnvwRuch5YAscF5EzxR601AEs%7C1627628360%7C931f090779804c4b660f4fe3b1cb6df0bd1470fa1a1108d7c29c6402c789e13f; MONITOR_WEB_ID=660b6b75-0e89-48dc-bc93-846eecc287a1; passport_csrf_token_default=6b0df0bccf20bb84d12d5a13444a7e4d; passport_csrf_token=6b0df0bccf20bb84d12d5a13444a7e4d; s_v_web_id=verify_krq22gb1_AiZgTTDi_sdQa_4dSP_9BXT_vOdrY3CXoDcI; n_mh=3TAsyBQ9TIOReANIuNLrZaSwE0wXPy61SN4Ofti2r3g; sso_uid_tt=08d76cd5e87300c1a152a44dd0f33709; sso_uid_tt_ss=08d76cd5e87300c1a152a44dd0f33709; toutiao_sso_user=3c3a357e34336ef5abb3e4d3f9e141e3; toutiao_sso_user_ss=3c3a357e34336ef5abb3e4d3f9e141e3; odin_tt=fe9555a871b1f2d454ab0c59132d8295d227ba95b31b11abc214e933a66b9a09acecbc283429b25294498235fcbea448; passport_auth_status_ss=89251bb56e23fe76bd94ec27fca95e03%2C; sid_guard=5a3787aa247d58f744cf3f8ae7ff3ad4%7C1627632070%7C5183999%7CTue%2C+28-Sep-2021+08%3A01%3A09+GMT; uid_tt=96ef0f175b69b8b55bb4f87d1db54267; uid_tt_ss=96ef0f175b69b8b55bb4f87d1db54267; sid_tt=5a3787aa247d58f744cf3f8ae7ff3ad4; sessionid=5a3787aa247d58f744cf3f8ae7ff3ad4; sessionid_ss=5a3787aa247d58f744cf3f8ae7ff3ad4; SID_UCP=5a3787aa247d58f744cf3f8ae7ff3ad4; SSID_UCP=5a3787aa247d58f744cf3f8ae7ff3ad4; passport_auth_status=89251bb56e23fe76bd94ec27fca95e03%2C'
cookie = {i.split("=")[0]: i.split("=")[1] for i in kuaishou_c.split(";")}
dy_cookies = {i.split("=")[0]: i.split("=")[1] for i in dy_cookies.split(";")}


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

kuaishou_search_request_data = {
    "operationName":"visionSearchPhoto",
    "variables":{
        "keyword":"猫咪",
        "pcursor":"",
        "page":"search"
    },
    "query":"query visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        photoUrl\n        liked\n        timestamp\n        expTag\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n"
}

# print("初始化爬虫")

save_path_prefix = '/Volumes/t2-ssd/douyin'
save_path_prefix = '/Users/shenghuang/Downloads/douyin'


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
