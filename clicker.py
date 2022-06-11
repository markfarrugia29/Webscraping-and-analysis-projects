from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="C:/ProgramFiles/Chrome_driver/chromedriver.exe", options=options)
driver.set_window_size(1120, 1000)

url = 'https://clickthatbutton.com/'
driver.get(url)
clicks = 0
    
while clicks < 10: 
        time.sleep(10)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.XPATH, "//form[@id='button']").click()
            clicks =+ 1
        except ElementClickInterceptedException:
            print("Couldn't find the button")
            pass