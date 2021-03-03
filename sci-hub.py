# 创建一个循环，为了能够连续下载文献
count = 1
for coount in range(1000):
    import requests
    from bs4 import BeautifulSoup
    import re
    from time import sleep

    # 输入doi，获取网页原代码(request.get)
    # 将int转化为str
    # print("第" + str(count) + "次执行")
    doi = input("请输入文献doi号后回车：")
    # doi = "10.1016/j.aquabot.2016.04.004"
    # 将输入的int转化为str，否则后面不识别
    doi = str(doi)
    print('\n' + "正在检索下载pdf文件，请耐心等待10s......")
    try:
        url = "https://scihub.wikicn.top/" + doi
        headers = {'user-agent': 'Chrome/10'}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = "utf-8"
    except:
        print("糟糕，检索失败 。请再尝试一次")
    # 解析网页原代码，获取pdf下载链接/url(BeautifulSoup)
    
    soup = BeautifulSoup(r.text, "html.parser")  # r.text为原代码
    for div in soup.select('div[id=citation]'):
        # 找出题目
        title = div.find('i').get_text()
        # 文件名不能包含下列任何字符：\ / : * ? " < > |
        # 提前将上面的字符其替换成空字符
        title = title.replace('/', '')
        title = title.replace(':', '')
        title = title.replace('<', '')
        title = title.replace('>', '')
        title = title.replace(';', '')
        title = title.replace('"', '')
        title = title.replace('?', '')
        # 给title最前面加一个.，提取.之间的字符串
        title = "." + title
        title = title.split('.')[1]
        # 此处有bug，遇到题目中有.的，就不能识别出完整的题目
        
        # 找出作者
        author = div.get_text()
        author = author.strip()  # 去除名字前面的空格
        author = ";" + author  # 考虑到作者的名和姓，所以选择了分号而不是逗号
        # 逗号遇到名在前就将整段字符筛选出来，所以选择了分号，只提取第一个作者
        author = str(author.split(';')[1])

        # 找出发表时间
        div = str(div)
        year = re.compile('\d')
        year = year.findall(div)
        year = year[0:4]
        year = "".join(year)  # list转str
        # 组合出文献名字
        title = str(title)
        paper_name = year + ' ' + title + '_' + author
    # 寻找并获取pdf链接
    for tag in soup.select('div[id=article]'):
        url = tag.find('iframe').get('src')
        # 通过对网页原代码进行分析，发现https有时不存在，故提前判断，若没有，就加上
        if 'http' not in url:
            url = "https:" + url
        else:
            url = url

    # 上面的代码已经获取pdf文件的url，接下来对其进行下载(requests.get)
        try:
            r = requests.get(url, timeout=60, headers=headers)
            r.raise_for_status()
            r.encoding = "utf-8"
        except:
            print("糟糕，检索失败 。请再尝试一次")
        sleep(5)  # 给pdf文件缓存留出5s的时间
    # 保存pdf文件到本地
        filename = paper_name + ".pdf"
        with open(filename, 'wb') as fb:
            fb.write(r.content)
        input('\n' + "下载已经完成，请按任意键进行下一次下载" + '\n')
    count = int(count)
    count += 1
# 以上就是此次代码的全部内容
# @ 1757765654@qq.com
