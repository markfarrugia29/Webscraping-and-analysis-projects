# Webscraping-and-analysis-projects
Files and notebooks aimed at webscraping using Selenium and subsequent data cleanup and analysis. 

**Resources used**
https://github.com/arapfaik/scraping-glassdoor-selenium - older version of selenium used to scrape glassdoor. I updated it and added some error exemptions, specifically for when the javascript refreshes and causes a StaleElementReferenceException

**Purpose** The main impetus of this project file was to help my wife analyze glassdoor salary postings for her field. Her field noticed that academic positions were going unfilled and she hypothesized the paygap between academic positions and private positions was growing too large. I decided to do a testrun with the field I was interested in first (Data Analyst) to sort out the bugs before running it on her field.

**Data collection** I pulled an old Selenium webscraping file from arapfaik (https://github.com/arapfaik/scraping-glassdoor-selenium) and updated it to remove depreciated files, added some fields such as salary min/max, and included some error exceptions. The main issue I ran into was a StaleElementReferenceException, which is when the element identified gets refreshed before you interact with it. This was resolved by including a try/except loop where the element would be identified by its position in the list index, reloaded, and interacted with again before returning back to the main loop. Glassdoor does have an API to use, so perhaps that would be an alternative route to take. I prepared three datasets with 1000 entries in each set. **One shortcoming currently is that I am not scraping the description and pulling keywords (Python, Git, etc.) for analysis - I hope to do this at a later date**.

**Data cleanup** The following was done to clean up the data: 
* Data was placed in a dataframe with pandas
* Empty cells filled with np.nan
* Rows with nulls for salary data were cleared
* Hourly rate marked with 0 (yearly) or 1 (hourly), then converted to yearly and changed to integers
* Company names were cleared of tailing /n strings
* City and State were placed in seperate columns
* The age of the company replaced the founding year

I still would like to pool the job titles to do a histogram analysis of the number of jobs per title (eg, jr data analyst vs sr data analyst), in addition to preparing a word-cloud of the most common skills requested per job. 

**Exploritory Data Analysis** - Pandas, Matplotlib.pyplot and Seaborn were used to analyze the cleaned dataset. Histograms for the average salary and rating showed a normal distribution about $75000 and 3.5 stars, respectively. Company age, unsurprisingly, had a harmonic curve decreasing from 0-200 years since founding. A small negative coorelation was observed between age and salary, and small positive for rating and salary (~-0.1 and 0.1, respectively). Pivot table analysis of all columns against the average salary showed that senior, cybersecurity and IT jobs pay the highest, with junior/entry-level analysts, underwriting analysts and research data analysts being on the lower end. Surprisingly, Georgia was highest on the states for salary, but this was largely due to the high number of cybersecurity/senior level positions being offered (44/52 positions). Lastly, large companies (5000+ employees) pay on the higher side, with the exception of 200-500 employee companies paying the highest. University/nonprofit jobs are at the bottom of the salary pool, with public companies and government work being the highest. Lastly, if the position has an hourly rate listed, it averages ~$10k less/year than salaried positions. 
