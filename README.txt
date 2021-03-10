# sci-hub desktop
# 个人编写，若有错误，请发邮件反馈1757765654@qq.com
# 利用python编写程序，输入doi号，自动下载文献（命名方式：时间+题目+作者）
# sci-hub网址：https://scihub.wikicn.top/


# 更新历史

【2021-3-10】
bug说明：今天下载文献，出现了一个小bug，提示为：title = div.find('i').get_text() AttributeError: 'NoneType' object has no attribute 'get_text' 
（没有找到<i>标签），在sci-hub.exe中，就是程序没有任何反应，就自动关闭
原因：翻看了具体的html源代码，发现代码里并没有有关文献的具体信息（上面的<i>标签就是为了获取文献的信息），所以才报错
解决办法：建议遇到这种情况手动打开网站下载，暂时还没想到具体的解决方法

【2021-3-3】
上传程序
