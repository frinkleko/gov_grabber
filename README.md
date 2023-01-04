# Gov grabber

## 撰写目的说明

本程序特为本人正在进行社会学研究的朋友撰写。考虑到人工重复机械下载繁琐耗时，因此撰写一个简单爬虫用于批量下载。本项目可以下载国内各县的财政数据。

## 用法

### 第一次运行

本程序依赖于python运行，对于任何需要使用本程序的用户，需要安装python和一些对应包。
使用分为以下几步：

1. 使用终端，切换至当前工作目录。（在终端中输入 cd 当前目录位置即可）
   例: cd D:\gov_grabber

2. 填写 xlsx表格

   结构为省、市、县、对应目录，备注。

   其中目录中各条目对应带有附件的单独新页面。可于本项目`data.xlsx`进一步查看。

3. 安装python和其对应包。
   首先你需要安装python。
     其次你需要安装 pandas, chardet, requests 。在终端中输入 pip install pandas chardet, requests 即可

4. 在终端中输入 python main.py 即可

### 后续使用

对于后续使用，仅需要更新`data.xlsx`后在在终端中输入 python main.py 即可。程序会跳过已经下载的文件（仍会打印下载信息）。
