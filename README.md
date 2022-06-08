# Webscraping-and-analysis-projects
Files and notebooks aimed at webscraping using Selenium and subsequent data cleanup and analysis. 

**Resources used**
https://github.com/arapfaik/scraping-glassdoor-selenium - older version of selenium used to scrape glassdoor. I updated it and added some error exemptions, specifically for when the javascript refreshes and causes a StaleElementReferenceException

**Purpose** The main impetus of this project file was to help my wife analyze glassdoor salary postings for her field. Her field noticed that academic positions were going unfilled and she hypothesized the paygap between academic positions and private positions was growing too large.

**Data collection** I pulled an old Selenium webscraping file from arapfaik (https://github.com/arapfaik/scraping-glassdoor-selenium) and updated it to remove depreciated files, added some fields such as salary min/max, and included some error exceptions. The main issue I ran into was a StaleElementReferenceException, which is when the element identified gets refreshed before you interact with it. This was resolved by including a try/except loop where the element would be identified by its position in the list index, reloaded, and interacted with again before returning back to the main loop. Glassdoor does had an API to use, so perhaps that would be an alternative route to take. I prepared three datasets with 1000 entries in each set. 


