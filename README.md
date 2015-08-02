# scrapy_for_seo
scrapy_for_seo

## 使用方法

1. 安装依赖：
    ```
    sudo pip install requests
    ```

1. 输入要爬取的关键字: 修改 run.py 中的 keyword，将关键字依次输入进去，格式为：keywords = ['天使汇', 'tech2ipo', '羊羊羊']

1. 修改 PAGE_COUNT = 2，修改为最多爬取多少页

2. 执行 run.py 脚本
    ```
    python run.py
    ```

## 结果查看

脚本执行完成后会生成如下文件/文件夹

```
html/
  pc_关键字_page_页码.html  
  zhidao_关键字_page_页码.html  
  mobile_关键字_page_页码.html  
PC.csv
zhidao.csv
mobile.csv
```

* html 目录中为爬取的网页的本地备份
* PC.csv 为 PC 端爬取结果
* mobile.csv 为手机端爬取结果
* zhidao.csv 为PC端百度知道爬取结果
