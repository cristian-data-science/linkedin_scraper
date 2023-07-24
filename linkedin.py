from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd



job_name = "Data Scientist"
country_name = "United States"

#We create the corresponding job name in URL
job_url ="";
for item in job_name.split(" "):
    if item != job_name.split(" ")[-1]:
        job_url = job_url + item + "%20"
    else:
        job_url = job_url + item
        
#We create the  corresponding country name in URL
country_url ="";
for item in country_name.split(" "):
    if item != country_name.split(" ")[-1]:
        country_url = country_url + item + "%20"
    else:
        country_url = country_url + item

url = "https://www.linkedin.com/jobs/search/?currentJobId=3634513412&geoId=103644278&keywords=computer%20science&location=Estados%20Unidos&refresh=true".format(job_url,country_url)

# Creating a webdriver instance
driver = webdriver.Chrome()
# Opening the url we have just defined in our browser
driver.get(url)



#We find how many jobs are offered.
jobs_num = driver.find_element(By.CSS_SELECTOR,"h1>span").get_attribute("innerText")
print(jobs_num)
if len(jobs_num.split(',')) > 1:
    jobs_num = (jobs_num.split(',')[0])*1000
else:
    jobs_num = (jobs_num)

jobs_num   = (jobs_num)

#Here I choose manually a number of jobs, so it wont take that long:
jobs_num = 1000


#We create a while loop to browse all jobs. 
i = 2
while i <= (jobs_num/2)+1:
    #We keep scrollind down to the end of the view.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    print("Current at: ", i, "Percentage at: ", ((i+1)/(int(jobs_num/2)+1))*100, "%",end="\r")
    try:
        #We try to click on the load more results buttons in case it is already displayed.
        infinite_scroller_button = driver.find_element(By.XPATH, ".//button[@aria-label='Load more results']")
        infinite_scroller_button.click()
        time.sleep(0.1)
    except:
        #If there is no button, there will be an error, so we keep scrolling down.
        time.sleep(0.1)
        pass



#We get a list containing all jobs that we have found.
job_lists = driver.find_element(By.CLASS_NAME,"jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME,"li") # return a list

#We declare void list to keep track of all obtaind data.
job_title_list = []
company_name_list = []
location_list = []
date_list = []
job_link_list = []

#We loof over every job and obtain all the wanted info.
for job in jobs:
    #job_title
    job_title = job.find_element(By.CSS_SELECTOR,"h3").get_attribute("innerText")
    job_title_list.append(job_title)
    
    
    #company_name
    company_name = job.find_element(By.CSS_SELECTOR,"h4").get_attribute("innerText")
    company_name_list.append(company_name)
    
    
    #location
    location = job.find_element(By.CSS_SELECTOR,"div>div>span").get_attribute("innerText")
    location_list.append(location)
    
    #date
    date = job.find_element(By.CSS_SELECTOR,"div>div>time").get_attribute("datetime")
    date_list.append(date)
    
    #job_link
    job_link = job.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
    job_link_list.append(job_link)

    print(job_title + str(" ") + company_name + str(" ") + location)
    #print(job_link)
    #time.sleep(0.01)
    #print("\n")
data = {'date': date_list,
        'company_name': company_name_list,
        'job_title': job_title_list,
        'location': location_list,
        'job_link': job_link_list}

df = pd.DataFrame(data)
df.to_excel('data_science_USA.xlsx')