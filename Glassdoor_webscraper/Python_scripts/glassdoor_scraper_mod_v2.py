from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException, StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    url = 'https://www.glassdoor.com/Job/' + keyword + '-jobs-SRCH_KO0,9.htm?context=Jobs&clickSource=searchBox'
    driver.get(url)
    jobs = []
    total_jobs = driver.find_element(By.CSS_SELECTOR, 'h1.hideHH.job-search-key-zga872.e15r6eig0').text
    print("There are ", total_jobs," for the input keyword(s).")
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except ElementClickInterceptedException:
            pass
        except WebDriverException:
            print("WebDriverException bypassed")
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.CSS_SELECTOR, "span.Close").click()  #clicking to the X. changed from find_element_by_css_selector
        except NoSuchElementException:
            pass

        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.XPATH, "//li[@data-test='jobListing']")  #  li for Job Listing. These are the buttons we're going to click.
        print("Populating button list")
        #initialize a counter to keep track of the position on the list "job_buttons". Needed in case you must reinitialize the list to avoid a StaleElementReferenceException
        cycle = 0
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            try:    
                job_buttons[cycle].click()
                cycle +=1
            except StaleElementReferenceException as Exception:
                print("StaleElementReferenceException while trying to click...seeking element again.")
                new_job_list = driver.find_elements(By.XPATH, "//li[@data-test='jobListing']")
                #print("Populating new list") #uncomment to print a statement showing you reinitialized a list
                new_job_list[cycle].click()
                    
                cycle +=1
                              
                
                
                pass
            time.sleep(1)
            collected_successfully = False
                               
            time.sleep(.1)

            try:
                driver.find_element(By.XPATH, "//span[@alt='Close']").click()  #clicking to the X. changed from find_element_by_css_selector
            except NoSuchElementException:
                pass
            
            while not collected_successfully:
                try:
                    print("Attempting to gather information")
                    company_name = driver.find_element(By.XPATH, ".//div[@class='css-xuk5ye e1tk4kwz5']").text
                    #print('The company name is ', company_name)
                    location = driver.find_element(By.XPATH, ".//div[@class='css-56kyx5 e1tk4kwz1']").text
                    #print('The company location is ', location)
                    job_title = driver.find_element(By.XPATH, ".//div[@class='css-1j389vi e1tk4kwz2']").text
                    #print('The company title is ', job_title)
                    #job_description = driver.find_element(By.XPATH, "//div[@class='jobDescriptioncontent desc']").text

                    collected_successfully = True
                except:
                    time.sleep(3)

            try:
                print("Looking for Information Container")
                driver.find_element(By.ID, 'JDCol')
                try:
                   
                    salary_estimate_min = driver.find_element(By.XPATH, ".//span[@class='css-1d4p0fd e2u4hf13']").text
                    #print("The minimum pay range is:", salary_estimate_min) # uncomment to print out a min salary while the code runs
                except NoSuchElementException:
                    salary_estimate_min = -1 #could use NA or NaN
                    #print("SALARY MIN NOT FOUND")
                try:
                    salary_estimate_max = driver.find_element(By.XPATH, ".//span[@class='css-1d4p0fd e2u4hf13']/following-sibling::span").text
                   # print("The maximum pay range is:", salary_estimate_max)
                except NoSuchElementException:
                    salary_estimate_max = -1 
                    #print("SALARY NOT FOUND")
                try:
                    salary_estimate_avg = driver.find_element(By.XPATH, ".//div[@class='css-y2jiyn e2u4hf18']").text
                    #print("The average pay range is:", salary_estimate_avg)
                except NoSuchElementException:
                    salary_estimate_avg = -1 
                    #print("SALARY NOT FOUND")
                try:
                    rating = driver.find_element(By.CLASS_NAME, 'css-1m5m32b.e1tk4kwz4').text
                    #print("The rating is:", rating)
                except NoSuchElementException:
                    rating = -1 
            except NoSuchElementException:
                
                salary_estimate_min = -1
                salary_estimate_max = -1
                salary_estimate_avg = -1
                rating = -1
                print("Could not find article")
                #print("RATING NOT FOUND")
            #Printing for debugging
            #if verbose:
            #    print("Job Title: {}".format(job_title))
            #    print("Salary Estimate: {}".format(salary_estimate))
            #    #print("Job Description: {}".format(job_description[ :500]))
            #    print("Rating: {}".format(rating))
            #    print("Company Name: {}".format(company_name))
            #    print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(By.XPATH, "//div[@id='CompanyContainer']").click()
                #try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    #headquarters = driver.find_element(By.XPATH, ".//span[@class=).text
                #except NoSuchElementException:
                    #headquarters = -1


                try:
                    size = driver.find_element(By.XPATH, ".//span[@class='css-1pldt9b e1pvx6aw1' and text()='Size']//following-sibling::span").text
                except NoSuchElementException:
                    #print("Failed to find company size")
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH,".//span[@class='css-1pldt9b e1pvx6aw1' and text()='Founded']//following-sibling::span").text
                except NoSuchElementException:
                    founded = -1
                    #print("Failed to find company founding date")

                try:
                    type_of_ownership = driver.find_element(By.XPATH,".//span[@class='css-1pldt9b e1pvx6aw1' and text()='Type']//following-sibling::span").text
                except NoSuchElementException:
                    type_of_ownership = -1
                    #print("Failed to find company ownership")

                try:
                    industry = driver.find_element(By.XPATH,".//span[@class='css-1pldt9b e1pvx6aw1' and text()='Industry']//following-sibling::span").text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH,".//span[@class='css-1pldt9b e1pvx6aw1' and text()='Sector']//following-sibling::span").text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,".//span[@class='css-1pldt9b e1pvx6aw1' and text()='Revenue']//following-sibling::span").text
                except NoSuchElementException:
                    revenue = -1
                
                #try:
                #    competitors = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                #except NoSuchElementException:
                #    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                #headquarters = -1
                print("NO COMPANY INFO FOUND")
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                #competitors = -1

                
            if verbose:
                #print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                #print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Minimum" : salary_estimate_min,
            "Salary Maximum" : salary_estimate_max,
            "Salary Average" : salary_estimate_avg,
            #"Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            #"Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #"Competitors" : competitors})
            #add job to jobs
        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, ".//span[@alt='next-icon']").click()
            time.sleep(3)
            #print("Page turned successfully")
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
    
    print("Stopping run")
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
    