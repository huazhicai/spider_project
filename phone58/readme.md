## 爬取58同城电销招聘信息，重点爬取招聘方电话号码

- **需要安装的软件**
    - python3.6
    - scrapy1.0
    - mysql5.7

- **遇到的问题**
    - 链接到详情页时遇到重定向，爬虫默认重定向不爬取，过滤了。
        - 解决思路：爬取企业uid, 然后构建url
    - 重构路径少了最后的 '/'的都不行，必须加上。
    - 他是先爬取好几个，再进行下一步，并不是说他不爬下个步骤，
    因为是多线程。调试过程中开启debug
    - 在浏览器中能找到定位到名企，在程序中死都返回不了，打印一下
    response.text 发现没有这个东东。浏览器和response毕竟存在一些差异。
    - in 操作符只用于sequence, 当对象为NoneType时，不可用
        - if mingqi and 'mingqi' in mingqi:
    - urlretrieve 下载图片总是遇到 error: no such file or directory
        - os.path.abspath('images') 获取到的绝对路径是错的，
        - 写真实的绝对路径，或者改为os.path.dirname(os.path.abspath(__file__))

- 搜索结果是7千条左右，但是70页无法全部展示，只有2千多条，
所以还要划分
    - 两种划分方式：
        - 按行业划分
        - 按区划分


- **做几个版本划分**
    - v1.0 基本爬虫，就是只用scrapy框架，不借助其他模块
    - v1.1 按行业划分。利用redis， 爬虫分为两个爬虫。
        - 第一个为industry_spider 爬取各行业的电话销售的url,存储到redis中(set)
        - 第二个phone_spder的初始url从redis中读取