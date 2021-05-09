
# Import libraries
#import os
import time
#import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import itertools


# Setting up helpful pandas options in case viewing the data (scraped pros/cons may be of significant length)
pd.set_option("display.max_rows", 2000)
pd.set_option("max_colwidth", 2000)

# Directives: limit_pages indicates whether one wants to scrape only a part of pages on a website (True) 
# or all of them (False)
limit_pages = True
# Set a number of pages to scrape (default = 100)
pages_no = 100


# Setting up helpful time functions to measure run-time and print start_time (in case ones forgot when exactly pressed 'run' button)
df_result_final = pd.DataFrame(columns=['review_id', 'pros', 'cons'])
start_time = time.time()
now = time.asctime()
print(now)


# Iterate over pages
if limit_pages:
    
    for y in range(1,pages_no+1):
        url='https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036_P'+str(y)+'.htm?filter.iso3Language=eng'
        
    #   setting User-Agent request header for letting the server identify operating system (here the token says that the browser is Mozilla-compatibile)   
        hdr = {'User-Agent': 'Mozilla/5.0'}  # Mozilla/5.0, Gecko/20100101
        req = Request(url,headers=hdr)
        page = urlopen(req)
        bs = BS(page, "html.parser")
        
        time.sleep(20) # set time sleeper after each page (to be polite)
        
        review_id_clean = []
        pros_clean = []
        cons_clean = []
            
        
        review_id = bs.find_all('span', attrs = {'data-disp-type':'review'})
        pros = bs.find_all('span', attrs = {'data-test':'pros'}) 
        cons = bs.find_all('span', attrs = {'data-test':'cons'}) 
        
    
        for x in review_id:
            y = str(x)
            m_cut = re.search('data-id="(.+?)" data-member', y) # find all strings that match regex pattern (are between 'data-id="' and '" data-member')
            if m_cut:
                rev = m_cut.group(1) # pick only first parenthesized subgroup
            review_id_clean.append(rev) # append the result to empty list
        
    
    
        for x in pros:
            if x == None or x == "": # replace possible nulls in pros/cons/both
                y = 'null'
            else:
                y = str(x.text).replace("\n", " ").replace("\r", " ").replace(";", " ") # replace semicolons with whitespaces so that it can be used later as delimiter
            pros_clean.append(y)
    
        for x in cons:
            if x == None or x == "":
                y = 'null'
            else:
                y = str(x.text).replace("\n", " ").replace("\r", " ").replace(";", " ")
            cons_clean.append(y)
    
        dict = {'review_id': review_id_clean, 'pros': pros_clean, 'cons': cons_clean} # create dictionary for final df
    
        df_result = pd.DataFrame(dict) # create pre-final df based on dictionary
        df_result_final = df_result_final.append(df_result) # append all pre-final dataframes to final dataframe

        
else:
    for y in itertools.count(start=1):
        
        url='https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036_P'+str(y)+'.htm?filter.iso3Language=eng'

    #   setting User-Agent request header for letting the server identify operating system (here the token says that the browser is Mozilla-compatibile)   
        hdr = {'User-Agent': 'Mozilla/5.0'}  # Mozilla/5.0, Gecko/20100101
        req = Request(url,headers=hdr)
        page = urlopen(req)
        bs = BS(page, "html.parser")
        
        time.sleep(20) # set time sleeper after each page (to be polite)
        
        review_id_clean = []
        pros_clean = []
        cons_clean = []
            
        
        review_id = bs.find_all('span', attrs = {'data-disp-type':'review'})
        pros = bs.find_all('span', attrs = {'data-test':'pros'}) 
        cons = bs.find_all('span', attrs = {'data-test':'cons'}) 

        if review_id == []:
            break
        
        else:
    
            for x in review_id:
                y = str(x)
                m_cut = re.search('data-id="(.+?)" data-member', y) # find all strings that match regex pattern (are between 'data-id="' and '" data-member')
                if m_cut:
                    rev = m_cut.group(1) # pick only first parenthesized subgroup
                review_id_clean.append(rev) # append the result to empty list
            
        
        
            for x in pros:
                if x == None or x == "": # replace possible nulls in pros/cons/both
                    y = 'null'
                else:
                    y = str(x.text).replace("\n", " ").replace("\r", " ").replace(";", " ") # replace semicolons with whitespaces so that it can be used later as delimiter
                pros_clean.append(y)
        
            for x in cons:
                if x == None or x == "":
                    y = 'null'
                else:
                    y = str(x.text).replace("\n", " ").replace("\r", " ").replace(";", " ")
                cons_clean.append(y)
        
            dict = {'review_id': review_id_clean, 'pros': pros_clean, 'cons': cons_clean} # create dictionary for final df
        
            df_result = pd.DataFrame(dict) # create pre-final df based on dictionary
            df_result_final = df_result_final.append(df_result) # append all pre-final dataframes to final dataframe

        
end_time = time.time() 

# Print run time
print("elapsed time:\n--- %s seconds ---" % (end_time - start_time))
print("--- %s minutes ---" % ((end_time - start_time)/60))
print("--- %s hours ---" % ((end_time - start_time)/3600))



# Save to csv file
df_result_final.to_csv('output_glassdoor_bs.csv', index=False, sep=';')



