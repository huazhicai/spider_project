## 爬取赶集网站上电话销售招聘企业信息
- 移动版的数据容易些，所以爬取移动版的
- 初始url : https://3g.ganji.com
- 第一层字段

|zh|en|
|---:|:---|
|标题|title|
|月薪|salary|
|公司名|company|

- 字段传递：meta={'item':item}
- 第二层字段

|zh|en|
|---:|:---|
|地址|address|
|电话|phone|
|联系人|contacts|

- 数据存储到mysql
- 使用随机用户
- 随机代理ip