from logging import root
import requests
import urllib3
urllib3.disable_warnings()
import re
from bs4 import BeautifulSoup
from time import sleep
from tkinter import *
from tkinter import messagebox


print("声明及操作如下：程序由个人编写、维护和更新，版本更新见网址 https://github.com/lu-wang-github/python_for_sci-hub。若程序闪退，请发送邮件反馈 1757765654@qq.com")
count = 0
for count in range(2000):
    count += 1
    print('\n'+ "正在执行第" + str(count) + "次文献下载" + '\n')
    doi = input("请输入文献链接（https://...）或doi（10...）后点击回车键：")
    print('\n' + "正在检索下载对应的pdf文件，请耐心等待5-15秒......")

    try:
        url = "https://sci-hub.mksa.top/" + str(doi)
        # url = "http://sci-hub.ren/" + str(doi)  #
        # url = "http://sci-hub.tf/" + str(doi)
        # headers = {'user-agent': 'Chrome/10'}  # 此处的user-agent不能用了，改换成Mozilla/5.0
        #headers = {'user-agent': 'Mozilla/5.0'}
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        r = requests.get(url,verify=False,timeout=60, headers=headers)
        r.raise_for_status()
        r.encoding = "utf-8"
    except:
        print("状态码" + str(r.status_code) + ", 唉！获取pdf失败,请再次尝试下载，或发送邮件反馈 1757765654@qq.com")
    sleep(0.5)

    if "article not found" in r.text:
        print('\n' + "唉！Sci-hub网站中没有找到对应的文献，请尝试别的途径下载！ 或再次尝试下载" + '\n')

    if "How to quickly find the DOI number of an article" in r.text:
        print('\n' + "唉！Sci-hub网站中没有找到对应的文献，请尝试别的途径下载! 或再次尝试下载" + '\n')
    elif "submit" in r.text:
        try:
            url = "http://sci-hub.tf/" + str(doi)
            headers = {'user-agent': 'Mozilla/5.0'}
            r = requests.get(url,verify=False, timeout=60, headers=headers)
            r.raise_for_status()
            r.encoding = "utf-8"
        except:
            print("状态码" + str(r.status_code) + ", 唉！获取pdf失败,请再次尝试下载，或发送邮件反馈 1757765654@qq.com")
        sleep(0.5)
    elif "submit" in r.text:
        try:
            url = "http://sci-hub.ren/" + str(doi)
            headers = {'user-agent': 'Mozilla/5.0'}
            r = requests.get(url,verify=False, timeout=60, headers=headers)
            r.raise_for_status()
            r.encoding = "utf-8"
        except:
            print("状态码" + str(r.status_code) + ", 唉！获取pdf失败,请再次尝试下载，或发送邮件反馈 1757765654@qq.com")
        sleep(0.5)
    else:
        
        soup = BeautifulSoup(r.text, "html.parser")
        for div in soup.select('div[id=citation]'):
            # 判断代码中是否有文献题目作者等相关信息
            if "." in str(div):
                if "<i>" in str(div):
                # 题目
                    title = div.find('i').get_text()
                    # 文件名不能包含下列任何字符：\ / : * ? " < > |，提前替换
                    title = title.replace('/', '')
                    title = title.replace('\r','')  # 删除字符串中的转义字符\r
                    title = title.replace('*','')
                    title = title.replace(':', '')
                    title = title.replace('<', '')
                    title = title.replace('>', '')
                    title = title.replace(';', '')
                    title = title.replace('"', '')
                    title = title.replace('?', '')
                    title = title.replace('|','')

                    # 给title最前面加一个.，提取.之间的字符串
                    title = "." + title
                    title = str(title.split('.')[1])
    
                    # 此处有bug，遇到题目中有.的，就不能识别出完整的题目
                    # 作者
                    author = div.get_text()
                    author = author.strip()  # 去除名字前面的空格
                    # 经过测试发现，如果作者是一个人，会报错，所以先将（更换为;
                    # 避免一个作者时报错，但对多个作者不影响
                    if ".," in author:
                        author = ".," + author
                        author = str(author.split('.,')[1])
                    else:
                        author = author.replace(' ' + '(', ';')
                        author = ";" + author  # 考虑到作者的名和姓，所以选择了分号而不是逗号
                        # 逗号遇到名在前就将整段字符筛选出来，所以选择了分号，只提取第一个作者
                        author = str(author.split(';')[1])
                    # 发表时间
                    div = str(div)
                    year = re.compile('\d')  # 正则表达，\d表示数字0-9
                    year = year.findall(div)
                    year = year[0:4]
                    year = "".join(year)  # list转str
                    # 组合出文献名字
                    paper_name = year + ' ' + title + '_' + author
                else:
                    title = doi.replace('/','')
                    paper_name = title
            else:
                    # 网页代码中，没有相关信息，就用文献的doi号作为题目
                title = doi.replace('/', '')
                paper_name = title
            sleep(0.5)
        
            # 寻找并获取pdf链接
            for tag in soup.select('div[id=article]'):
                # 判断tag是旧文献链接还是新文献链接
                # 将标签（tag）转化为字符串，条件函数判断字符串中是否有新文献特有的字符，例如embed/type
                # 第一次使用的条件判断语句为if “iframe” in tag, 报错；可能是tag没有转化为str(tag)
                if "embed" in str(tag):
                    url = tag.find('embed').get('src')
                else:
                    url = tag.find('iframe').get('src')
                
                # 网页原代码分析发现https有时不存在，故提前判断，若没有，就加上
                if 'http' not in url:
                    url = "https:" + url
                else:
                    url = url
                sleep(0.5)

            # 上面的代码已经获取pdf文件的url，接下来对其进行下载(requests.get)
            try:
                r = requests.get(url, timeout=90, headers=headers)
                r.raise_for_status()
                r.encoding = "utf-8"
            except:
                print("状态码" + str(r.status_code) + ",唉！请再次尝试下载，或发送邮件反馈 1757765654@qq.com")
            sleep(1)  # 给pdf文件缓存留出5s的时间

        # 保存pdf文件到本地
            filename = paper_name + ".pdf"
            with open(filename, 'wb') as fb:
                fb.write(r.content)
            input('\n' + "哈哈！检索的文献已经下载到本地（和程序在同一文件夹中），按下回车键启动下一次的下载" + '\n')
# 联系作者1757765654@qq.com
#不足：无法实现对网站内容的嗅探，一旦当前的网址不能使用，软件就无法运行了。
#所以，最好就是能做出页面，提供网址选择。或者一旦有故障，让软件自行匹配合适的网址
