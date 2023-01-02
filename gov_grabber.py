import requests 
import re
from bs4 import BeautifulSoup
import os
import sys

# for encoding detection
import chardet

def downloader(herf,folder_name,main_url = None,encoding = 'gbk'):
    # refill the url with main url if it is missing
    try:
        req = requests.get(herf)
    except requests.exceptions.MissingSchema:
        try:
            req = requests.get(main_url + herf)
        except:
            req = requests.get(main_url + '/' + herf)
    except:
        return 

    # most of the time, the encoding is gbk
    req.encoding = encoding
    soup = BeautifulSoup(req.text, "html.parser")
    all_a = soup.find_all('a')

    # filter out the file with the extention
    file_extentions = ['pdf','doc','docx','xls','xlsx','rar','zip']

    for file_extention in file_extentions:
        for a in all_a:
            herf_ = a.get('href')
            if not herf_:
                continue
                
            # filter all herf with the extention
            file_pattern = ".*." + file_extention + "$"
            filtered_href = re.match(file_pattern, herf_)

            # get file name
            if filtered_href:
                file_name = a.string
                if file_name == None:
                    file_name = str(a).split('<br/>')[0].split('>')[1]
                
                # filter out the chinese characters and numbers
                file_name = re.sub("[^\u4e00-\u9fa5^0-9]", "", file_name)

                # download the file
                print('Downloaing {}.{}...'.format(file_name,file_extention))

                # check if the file exists
                if not os.path.exists(folder_name+'/'+'{}.{}'.format(file_name,file_extention)):

                    # download the file
                    with open(folder_name+'/'+'{}.{}'.format(file_name,file_extention),'wb') as f:
                        try:
                            response = requests.get(filtered_href.string)
                        except requests.exceptions.MissingSchema:
                            try:
                                response = requests.get(main_url + herf)
                            except:
                                response = requests.get(main_url + '/' + herf)
                        f.write(response.content)

def gov_grabber(url = None, folder_name = None, file_extention = 'pdf'):

    # use command line to input url and folder name
    if len(sys.argv)<2 and (url == None or folder_name == None):
        print("Please input the url and folder name")
        return
    
    # get the main url
    main_url = url.split('/col')[0]
    if main_url == url:
        main_url = url.split('/')
        for i in main_url:
            if i.endswith('.cn'):
                main_url = i
                break
    if not main_url.startswith('http'):
        main_url = 'http://' + main_url
    print(main_url)

    # process the first page
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    req = requests.get(url,headers = {'User-Agent': UA})

    # detect the encoding
    result = chardet.detect(req.content)
    req.encoding = result['encoding']

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
        if herf.startswith('javascript'):
            continue
        # just download if not success this function will just return nothing
        downloader(herf,folder_name,main_url,encoding = req.encoding)

if __name__ == '__main__':
    gov_grabber(url = 'http://www.dingxing.gov.cn/czyslist-394-more.html',folder_name = 'test')