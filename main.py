from gov_grabber import gov_grabber
import pandas as pd
import os

# read target xlsx
data = pd.read_excel('data.xlsx')
# rename columns
data.columns = ['province','city','country','url']
# get unique citys
citys = data['city'].unique()
province = data['province'].unique()

# for each province, create a folder
for pro in province:
    if not os.path.exists(pro):
        os.mkdir(pro)
        os.chdir(pro)
    else:
        print("The {} folder already exists".format(pro))
        os.chdir(pro)
    
    # for each city, create a folder and download files
    for city in citys:
        data_city = data[data['city'] == city]
        if not os.path.exists(city):
            os.mkdir(city)
            os.chdir(city)
        else:
            print("The {} folder already exists".format(city))
            os.chdir(city)

        # for each country, download files
        for index, row in data_city.iterrows():
            gov_grabber(url = row['url'],folder_name = row['country'])
        os.chdir('..')

    # exit the city folder
    # and enter the province folder
    os.chdir('..')