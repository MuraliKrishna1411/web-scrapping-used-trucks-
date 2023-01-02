from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time                                                   # importing all libraries
time.sleep(3)
dr = webdriver.Chrome()

dr.maximize_window()
dr.get('https://www.motorbazee.com/')

element= dr.find_element_by_id('SerchMakeBlogTruck')
drp = Select(element)
all_Truck = drp.options
Trucks=[]                                                    # creating Trucks list    

for i,j in zip(all_Truck,range(0,100)):
    try:
        Trucks.append(f'--{j}-- {i.text}')
    except:
        pass
print(*Trucks,sep="\n")
Vehicle_index= int(input('enter vehicle index :    '))                # selecting Truck
drp.select_by_index(Vehicle_index)

element1= dr.find_element_by_id('SerchModelBlogTruck')
drp1 = Select(element1)

all_Model = drp1.options
Models=[]

for i,j in zip(all_Model,range(0,1000)):
    try:
        Models.append(f'--{j}-- {i.text}')

    except:
        pass
print(*Models,sep="\n")
Model_index= int(input('enter Model index :    '))                     # Selecting Model
drp1.select_by_index(Model_index)

x = dr.find_element_by_id('UsedTruckSubmit')
y = x.click()
# df=webdriver.(dr.find_element_by_id('UsedTruckSubmit').click())
from selenium.webdriver.common.by import By

s='document.querySelector("body > div:nth-child(15) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h4:nth-child(1) > a:nth-child(1)").baseURI'
s1=dr.execute_script('return'+' '+s)                   
raw= s1                                                                 # gettomg url using random buttuon 
page = requests.get(s1)
print(page)

soup = BeautifulSoup(page.content,'html.parser')
                                                                          # this will bring all the data from the url
a_tags= soup.find_all('a')

j=[]
for tag in a_tags:
    a=tag['href']
    j.append(a)

s= 'used-truck+'                                                          # using filter in data extracted
k=[]
for i in j:
    if s in i:
        k.append(i)

time.sleep(2)
Price=[]
raw2=[]
for i in k:
    dr.get(i)
    sc='document.querySelector("body > div:nth-child(12) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5)")'
    sc2 = dr.execute_script('return'+' '+sc)
    raw = sc2.text
    t = dr.find_element_by_xpath("//h3[contains(text(),'Price')]")
    raw1=t.text
    raw2.append(raw)
    Price.append(raw1)                    # data is extracted in raw format

time.sleep(2)

n=[]
for i in raw2:
    if 1>0:
        x=i.split('\n')
        n.append(x)                                       # splitting and appending

time.sleep(1)
Model = []
Fuel = []
Odometer = []
Insurance = []
State = []
City = []
Vehicle = []
mfo = [Model,Fuel,Odometer,Insurance,State,City,Vehicle]
mf = ['Model','Fuel','Odometer','Insurance','State','City','Vehicle ID']

time.sleep(1)
for i in range(len(n)):
        for j,h in zip(mfo,mf):
            try:
                x=n[i]                                                         # using 2 variable in single loop to complete all the data insertion into columns
                j.append(x[(x.index(h)+1)])                                   
            except:
                j.append('nan')

time.sleep(2)
MotorBazee = pd.DataFrame({'Model':Model,'Fuel':Fuel,'Odometer':Odometer,'Insurance':Insurance,'State':State,'City':City,'Vehicle ID':Vehicle,'Price':Price})          #creating a datafrmae
m=MotorBazee
m[['Price1','Price2']]=m.Price.str.split(' ',expand=True)
m.drop(['Price','Price1'],axis=1,inplace=True)
m.rename(columns={"Price2":'Price'},inplace=True)
MotorBazee=m
print(MotorBazee)
MotorBazee.to_csv(f'MotorBazeefinal.csv {Vehicle_index} {Model_index}')                # creatubg csv using vehicle idex and model index