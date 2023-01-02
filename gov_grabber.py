import requests 
import re
from bs4 import BeautifulSoup
import os
import sys

def downloader(herf,folder_name,main_url = None):
    try:
        req = requests.get(herf)
    except requests.exceptions.MissingSchema:
        req = requests.get(main_url + herf)
    req.encoding = 'gbk'
    soup = BeautifulSoup(req.text, "html.parser")
    all_a = soup.find_all('a')
    file_extentions = ['pdf','doc','docx','xls','xlsx','rar','zip']
    for file_extention in file_extentions:
        for a in all_a:
            herf_ = a.get('href')
            if not herf_:
                continue
            file_pattern = ".*." + file_extention + "$"
            filtered_href = re.match(file_pattern, herf_)
            if filtered_href:
                file_name = a.string
                if file_name == None:
                    file_name = str(a).split('<br/>')[0].split('>')[1]
                # 过滤出中文和数字
                file_name = re.sub("[^\u4e00-\u9fa5^0-9]", "", file_name)
                print('Downloaing {}.{}...'.format(file_name,file_extention))
                if not os.path.exists(folder_name+'/'+'{}.{}'.format(file_name,file_extention)):
                    with open(folder_name+'/'+'{}.{}'.format(file_name,file_extention),'wb') as f:
                        try:
                            response = requests.get(filtered_href.string)
                        except requests.exceptions.MissingSchema:
                            response = requests.get(main_url  + filtered_href.string)
                        f.write(response.content)

def gov_grabber(url = None, folder_name = None, file_extention = 'pdf'):

    if len(sys.argv)<2 and (url == None or folder_name == None):
        print("Please input the url and folder name")
        return
    
    main_url = url.split('/col')[0]
    print(main_url)

    #file_extentions = ['pdf','doc','xls']

    # process the first page
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    all_a = soup.find_all('a')

    # create the folder
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        print("The {} folder already exists".format(folder_name))

    for a in all_a:
        herf = a.get('href')
        # process second page
        if not herf:
            continue

        if herf.split('/')[-1] == 'index.html' or not herf.endswith('.html'):
            continue
        downloader(herf,folder_name,main_url)

if __name__ == '__main__':
    gov_grabber(url = 'http://www.sjzjx.gov.cn/col/1580696057686/index.html',folder_name = 'test')