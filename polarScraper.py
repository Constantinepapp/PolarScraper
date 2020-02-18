from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import time 
import csv
import pandas as pd
from dateutil.parser import parse


# this function tranforms "hr:min:sec" string to float number
def time_to_float_number(duration):
    duration=parse(duration)
    float_time=(duration.hour*60)+duration.minute+(duration.second)/60
    float_time=round(float_time,2)
    return float_time



print("Enter a polar flow activity url: ")
user_input_link=input()
user_email=input("Enter your email : ")
user_pass=input("Enter your password : ")
webdriver= "chromedriver.exe"

driver=Chrome(webdriver)


url= user_input_link
driver.get(url)

email=driver.find_element_by_css_selector('#email')
password=driver.find_element_by_css_selector('#password')
enter=driver.find_element_by_css_selector('#login')

email.send_keys(user_email)
password.send_keys(user_pass)
enter.click()

print("How many activities do you want to save?")
numact=int(input())
i=1

time.sleep(3)
content =driver.page_source

while i <= numact:
    head=driver.find_element_by_id('sportHeading').text
    try:
        if "Running" in head:
            
            duration=driver.find_element_by_id('duration').get_attribute("value")
            distance=driver.find_element_by_id('BDPDistance').text
            Heart_rate=driver.find_element_by_id('BDPHrAvg').text
            AvSpeed=driver.find_element_by_id('BDPSpeedAvg').get_attribute('innerText')

            # this 3 values are possible to not exist in some runs
            try:
                Running_index=driver.find_element_by_css_selector("#trainingDetailsContainerBox > div > div.col-md-8.col-md-push-4.exercise-statistics-wrapper > fieldset > div > div > aside.col-md-4.col-sm-4.col-xs-12.clearfix.RUNNINGINDEX > div.basic-data-panel__value > span.basic-data-panel__value-container").get_attribute('innerText')
            except:
                Running_index=0
                print("Running index not found, default value 0")
            try:    
                down=driver.find_element_by_css_selector('#trainingDetailsContainerBox > div > div.col-md-8.col-md-push-4.exercise-statistics-wrapper > fieldset > div > div > aside.col-md-4.col-sm-4.col-xs-12.clearfix.DESCENT > div.basic-data-panel__value > span.basic-data-panel__value-container').get_attribute('innerText')
            except:
                down=0
                print("descent not found, default value 0")

            try:   
                up=driver.find_element_by_css_selector('#trainingDetailsContainerBox > div > div.col-md-8.col-md-push-4.exercise-statistics-wrapper > fieldset > div > div > aside.col-md-4.col-sm-4.col-xs-12.clearfix.ASCENT > div.basic-data-panel__value > span.basic-data-panel__value-container').get_attribute('innerText')
            except:
                up=0
                print("Ascent not found, default value 0")

                
            distance=float(distance)*1000


            # the lines below take a date of format '30 oct ,2019,20:12) and make a string of '2019-10-30' format
            typ,date_device=head.split('\n')
            dater,device=date_device.split('|')
            dater=parse(dater)
            dater=dater.strftime('%Y-%m-%d')

            duration=time_to_float_number(duration)
            row=[dater,duration,distance,Heart_rate,AvSpeed,Running_index,up,down]
            print(row)
            
        
            with open("run.csv", "a", newline="") as file:
                writer=csv.writer(file)
                writer.writerow(row)
        
            file.close()
    
        else:
            print("Non run type")
        
    except:
        print("Something went wrong with this activity :",head,", moving to next")
    
    i=i+1
    url=driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div[1]/div/ul/li[1]/a").get_attribute("href")
    driver.get(url)
    time.sleep(3)

print("Scraping Completed!")



    
   