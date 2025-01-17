
## importing libraries
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

## importing libraries to plot the wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

## Linkedin ID and PASSWORD
email = "email"
password = "password"

## Write here the job position and local for search
position = "Machine Learning Engineer"
local = "United States"

## formating to linkedin model
position = position.replace(' ', "%20")



options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_window_size(1024, 600)
driver.maximize_window()

## Opening linkedin website
driver.get('https://www.linkedin.com/login')



#Import exception check
from selenium.common.exceptions import NoSuchElementException
try:
    if driver.find_element(By.CLASS_NAME,'msg-overlay-list-bubble--is-minimized') is not None:
        pass
except NoSuchElementException:
    try:
        if driver.find_element(By.CLASS_NAME,'msg-overlay-bubble-header') is not None:
            driver.find_element(By.CLASS_NAME,'msg-overlay-bubble-header').click()
    except NoSuchElementException:
        pass

## waiting load
time.sleep(2)

## Search for login and password inputs, send credentions 
driver.find_element('id','username').send_keys(email)
driver.find_element('id','password').send_keys(password)
driver.find_element('id','password').send_keys(Keys.RETURN)

## Opening jobs webpage
driver.get(f"https://www.linkedin.com/jobs/search/?currentJobId=3480674131&distance=25&geoId=103644278&keywords={position}")
## waiting load
time.sleep(2)





## creating a list where the descriptions will be stored
desc_list = []

## each page show us some jobs, sometimes show 25, others 13 or 21
## with this knowledge I created a loop that will check how many jobs the page is listing
## Then 

## linkedin in general displays 40 jobs pages, then we loop over 40 times to get all the job profiles. 
for i in range(1,41):
    ## click button to change the job list
    driver.find_element('xpath',f'//button[@type="button" and @aria-label="Page {i}"]').click()
    ## each page show us some jobs, sometimes show 25, others 13 or 21 ¯\_(ツ)_/¯
    jobs_lists = driver.find_element(By.CLASS_NAME,'scaffold-layout__list-container') #here we create a list with jobs
    jobs = jobs_lists.find_elements(By.CLASS_NAME,'jobs-search-results__list-item') #here we select each job to count
    ## waiting load
    time.sleep(2) 
    ## the loop below is for the algorithm to click exactly on the number of jobs that is showing in list
    ## in order to avoid errors that will stop the automation
    for job in range (1, len(jobs)+1):
        ## job click

        print(f'Job {job}')
        
        driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{job}]').click()
        ## waiting load 
        time.sleep(1)

        driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{job}]/div/div[1]/div[1]/div[2]/div[1]/a').click()
        time.sleep(1)

        ## select job description
        job_desc = driver.find_element(By.ID, 'job-details')

        #get text
        soup = BeautifulSoup(job_desc.get_attribute('outerHTML'), 'html.parser')
        ## add text to list
        desc_list.append(soup.text)


# Creating a Dataframe with list
df = pd.DataFrame(desc_list)

df.to_csv('job_desc.csv')
