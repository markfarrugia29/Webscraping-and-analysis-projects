from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def click_button(path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://clickclickclick.click/#e497d52ad16fc591c360856eb39d3dc5'
    driver.get(url)
    clicks = 0
    
    while clicks < 4: 

        time.sleep(slp_time)
        driver.find_element(By.CLASS_NAME, "button").click()
        print("Button clicked successfully", clicks + 1 ,"times")
        clicks += 1
        if clicks == 4:
            print("I'm done clicking the button now. Time to rest! ZzZzZz")

        