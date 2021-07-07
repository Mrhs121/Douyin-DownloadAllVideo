# Douyin-DownloadAllVideo
Easily download all the videos from TikTok.下载指定的抖音号的所有视频，爬虫

# Requirement
  * python
  * selenium
  * BeautifulSoup

# 用法

打开 `https://www.douyin.com` ，搜索你需要下载的up主，将up主主页链接粘贴至`douyin_url.txt`文件中，可以同时下载多个up，每个up的链接独占一行，
文件最后一行用`##end##`结尾

此处用冯提莫作为例子：

https://www.douyin.com/user/MS4wLjABAAAAbgCnupO_NGaTAmzWnXSivCeHWrOe0wC2ZcpNvVoQfEk?extra_params=%7B%22search_id%22%3A%22202107072151000102121640354914D12F%22%2C%22search_result_id%22%3A%2258958068057%22%2C%22search_keyword%22%3A%22%E5%86%AF%E6%8F%90%E8%8E%AB%22%2C%22search_type%22%3A%22video%22%7D&enter_method=search_result&enter_from=search_result

 然后直接运行 python douyin.py 即可开始下载
 
 
