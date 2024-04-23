倒余额脚本获取最优且较稳定的策略

输入需要查找的成交量，以及金额的范围查找目标饰品

设计原理

访问(https://www.iflow.work/cn?platform=buff-igxe-c5-uuyp&game=csgo-dota2&order=sell&pagenum=1&min_price=1.0&max_price=5000.0&min_volume=200)

其中min price代表最小金额 max price为最大金额为浮点数，min volume为最近成交量

只去查找符合条件的前面五十条 查看他的目标金额 是否金额过期， 若过期算出新的折扣，排序后显示在网页

（五十条爬取可能有等待时间，可以只看前面十条）

因为只用buff和悠悠，筛选过滤掉其他的平台

若三个参数都不输入 默认参数为这个

(https://www.iflow.work/cn?platform=buff-uuyp&game=csgo-dota2&order=sell&pagenum=1&min_price=1.0&max_price=5000.0&min_volume=100)



所以需要的价格有三个，buff平台的实时价格和悠悠平台的实时价格以及steam平台的实时价格，因为悠悠平台查看价格需要登陆信息，需要特殊处理



技术问题 解决uu的登录问题 方法一，使用Cookie注入爬取，用户需要自行在网站上登陆然后把Cookie信息输入在网站

​													方法二，使用selenium爬取，打开浏览器登录后，再软件点击确认按钮开始爬取信息

