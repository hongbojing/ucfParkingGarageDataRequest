from lxml import html
import requests
import re
import pandas as pd
import os
import csv
from IPython.display import clear_output
import datetime
import matplotlib.pyplot as plt
import time
def get_data(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    garage=[]
    garageName=[]
    garageTotalSpace=[]

    #This will create a list of buyers:
    name = tree.xpath('//td[@class="dxgv"]/text()')
    space = tree.xpath('//td[@class="dxgv"]/strong/text()')
    results = map(int, space)
    for row in name:
        #match = re.search(r'\bGarage\b',row)
        if "Garage" in row:
            garageName.append(row)

        elif any(char.isdigit() for char in row):
            rowNumebr=int(filter(str.isdigit, row))
            garageTotalSpace.append(rowNumebr)
    garage.append(garageName)
    garage.append(space)
    garage.append(garageTotalSpace)
    df = pd.DataFrame({
    'name':garageName,
    'empty':space,
    'total':garageTotalSpace
})
    return df 
#-----------------------------main----------------------------------------------

url='http://secure.parking.ucf.edu/GarageCount/'
data=get_data(url)
start_time=datetime.datetime.now()
#create folder
if os.path.exists('data'):
    print("file data exist")
else:
    print("file data not exist,created")
    os.mkdir('data')
if os.path.exists('data/parking'):
    print("file data/parking exist")
else:
    os.mkdir('data/parking')
    print("file data/parking not exist,created")
csvKeys=["index",
         "empty",
        'name', 
        'total',
        'time' ]   
if os.path.exists('data/parking/parkingRaw.csv'):
    print("file data/parking/parkingRaw.csv exist")
else:
    with open('data/parking/parkingRaw.csv', 'wb') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames = csvKeys)
        writer.writeheader()
        
    outcsv.close()
    print("file data/parking/parkingRaw.csv not exist,created")
counter=0

while True:
    counter+=1
    clear_output(wait=True)
    temp_time=datetime.datetime.now()
    print("start time:"+str(start_time) +" - "+str(temp_time))
    print("already collected : "+str(counter))
    url='http://secure.parking.ucf.edu/GarageCount/'
    data=get_data(url)
    data['time'] = datetime.datetime.now()
    print data
    data.to_csv('data/parking/parkingRaw.csv', mode='a', header=False)
    time.sleep(60)
    #os.system( 'cls' )