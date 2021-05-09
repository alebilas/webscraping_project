# Import libraries
from selenium import webdriver
import time
import getpass
import datetime
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

# Directives: limit_pages indicates whether one wants to scrape only a part of pages on a website (True) 
# or all of them (False)
limit_pages = True
# Set a number of pages to scrape (default = 100)
pages_no = 100

# Define path to a driver
chrome_path = 'C:\\Users\\aleksandra.bilas\\chromedriver.exe'

# Set website URL
url = 'http://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm'

# Set driver options
options = webdriver.chrome.options.Options()
options.headless = False

# Define driver
driver = webdriver.Chrome(options = options, executable_path = chrome_path)
# Maximize browser window
driver.maximize_window()

time.sleep(20)
driver.get(url)

print('Page ready')

time.sleep(10)

#################### LOGIN ####################
# Click on Accept cookies button
button = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
button.click()

time.sleep(5)

# Click on singin button
button = driver.find_element_by_xpath('//*[@id="SignInButton"]/button')
button.click()

time.sleep(5)

# Input email address
username = driver.find_element_by_xpath('//*[@id="userEmail"]')
my_email = input('Please provide your email:')
username.send_keys(my_email)

time.sleep(5)

# Input password
password = driver.find_element_by_xpath('//*[@id="userPassword"]')
my_pass = getpass.getpass('Please provide your password:')
password.send_keys(my_pass)

time.sleep(5)

# Click on Sign In button
button = driver.find_element_by_xpath('//*[@id="LoginModal"]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/form/div[3]/div[1]/button')
button.click()

time.sleep(20)
# print(driver.page_source)

##### ACTUAL PROGRAM #####

if limit_pages: # If a user wants to scrape a part of pages (limit_pages == True)
    iter = 0 #set iterator for information printing
    review_id_list = [] # create an empty list for all reviews (it will be updated after each page scraping)
    pros_list = [] # create an empty list for all pros (it will be updated after each page scraping)
    cons_list = [] # create an empty list for all cons (it will be updated after each page scraping)

    start_time = time.time() # save start time

    while iter < pages_no: # Iterate until all 100 pages are scraped

        print(f"Scraping the page number {iter+1}.")

        # Create a list of all elements containing review ID information
        reviews_elements = driver.find_elements_by_class_name("flagContent")
        # Create a list of all elements containing pros
        pros_elements = driver.find_elements_by_xpath("//span[@data-test='pros']")
        # Create a list of all elements containing pros
        cons_elements = driver.find_elements_by_xpath("//span[@data-test='cons']")

        try: # Retrieve review ID from each element from the list of reviews 
            for i in range(0, len(reviews_elements)):
                rev = reviews_elements[i].get_attribute('data-id').replace("\n", " ").replace("\r", " ").replace(";", " ")
                review_id_list.append(rev)
        except: # If there is no review ID, put 'null'
            review_id_list.append('null')

        try: # Retrieve a pro from each element from the list of pros
            for i in range(0, len(pros_elements)):
                pro = pros_elements[i].text.replace("\n", " ").replace("\r", " ").replace(";", " ")
                pros_list.append(pro)
        except: # If there is no review ID, put 'null'
            pros_list.append('null')

        try: # Retrieve a con from each element from the list of cons
            for i in range(0, len(cons_elements)):
                con = cons_elements[i].text.replace("\n", " ").replace("\r", " ").replace(";", " ")
                cons_list.append(con)
        except: # If there is no review ID, put 'null'
            cons_list.append('null')

        iter = iter+1 # Add 1 to the iterator

        try: 
            # Find the Next button
            next_link = driver.find_element_by_xpath('//button[@data-test="pagination-next"]')
            # Get coordinates of the button
            coor_Y = next_link.location.get('y')
            # Substract 450 pixels from the Y coordinate (ensuring that the button is visible)
            coor_Y_new = coor_Y-450

            # Scroll to the top of the website
            driver.execute_script('window.scrollBy(0, -9000)') 
            # Scrolling the place on the page to ensure that the Next button is visible 
            driver.execute_script(f'window.scrollBy(0, {coor_Y_new})')
            
            # Click on the Next button
            next_link.click() 
            time.sleep(20)
        except NoSuchElementException: 
            print('End of scraping.')                
else: # If a user wants to scrape all of pages (limit_pages == False)
    iter = 0 #set iterator for information printing
    review_id_list = [] # create an empty list for all reviews (it will be updated after each page scraping)
    pros_list = [] # create an empty list for all pros (it will be updated after each page scraping)
    cons_list = [] # create an empty list for all cons (it will be updated after each page scraping)

    start_time = time.time() # save start time

    while limit_pages: # Run the code until all pages are scraped (reuse of the limit_pages flag to limit parameters)
        limit_pages = True 

        print(f"Scraping the page number {iter+1}.")

        # Create a list of all elements containing review ID information
        reviews_elements = driver.find_elements_by_class_name("flagContent")
        # Create a list of all elements containing pros
        pros_elements = driver.find_elements_by_xpath("//span[@data-test='pros']")
        # Create a list of all elements containing pros
        cons_elements = driver.find_elements_by_xpath("//span[@data-test='cons']")

        try: # Retrieve review ID from each element from the list of reviews 
            for i in range(0, len(reviews_elements)):
                rev = reviews_elements[i].get_attribute('data-id')
                review_id_list.append(rev)
        except: # If there is no review ID, put 'null'
            review_id_list.append('null')

        try: # Retrieve a pro from each element from the list of pros
            for i in range(0, len(pros_elements)):
                pro = pros_elements[i].text
                pros_list.append(pro)
        except: # If there is no review ID, put 'null'
            pros_list.append('null')

        try: # Retrieve a con from each element from the list of cons
            for i in range(0, len(cons_elements)):
                con = cons_elements[i].text
                cons_list.append(con)
        except: # If there is no review ID, put 'null'
            cons_list.append('null')

        iter = iter+1 # Add 1 to the iterator

        try: 
            # Find the Next button
            next_link = driver.find_element_by_xpath('//button[@data-test="pagination-next"]')
            # Get coordinates of the button
            coor_Y = next_link.location.get('y')
            # Substract 450 pixels from the Y coordinate (ensuring that the button is visible)
            coor_Y_new = coor_Y-450

            # Scroll to the top of the website
            driver.execute_script('window.scrollBy(0, -9000)') 
            # Scrolling the place on the page to ensure that the Next button is visible 
            driver.execute_script(f'window.scrollBy(0, {coor_Y_new})')
            
            # Click on the Next button
            next_link.click() 
            time.sleep(20) 
        except NoSuchElementException: 
            limit_pages = False # if there are no other pages then stop the process
            print('No pages remaining. End of scraping.')      

# Close browser
driver.quit()

# Create a dictionary of all retrieved values
dict = {'review_id': review_id_list, 'pros': pros_list, 'cons': cons_list} 

# Insert all lists to a data frame
df_result = pd.DataFrame(dict)

# save end time
end_time = time.time()

df_result.to_csv(os.path.join(os.getcwd(), 'selenium_output.csv'), index=False, sep=';')

print(f'{iter} pages were scraped. The output file was saved in {os.getcwd()}. End of the process.')

# Show time
print("----- The process took %s minutes -----" % ((end_time - start_time)/60))

# 10s/100p - 18 min
# 20s/100p -  34 min