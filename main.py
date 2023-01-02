from gov_grabber import gov_grabber
import pandas as pd
import os

data = pd.read_excel('data.xlsx')
data.columns = ['city','country','url']
citys = data['city'].unique()
for city in citys:
    data_city = data[data['city'] == city]
    if not os.path.exists(city):
        os.mkdir(city)
        os.chdir(city)
    else:
        print("The {} folder already exists".format(city))
        os.chdir(city)
    for index, row in data_city.iterrows():
        gov_grabber(url = row['url'],folder_name = row['country'])
    os.chdir('..')