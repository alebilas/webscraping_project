
# Import libraries
import scrapy
import pandas as pd
import os
import time
import itertools

# Directives: limit_pages indicates whether one wants to scrape only a part of pages on a website (True) 
# or all of them (False)
limit_pages = True
# Set a number of pages to scrape (default = 100)
pages_no = 100


# Iterate over pages
if limit_pages:
    
    links = ['https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036_P%s.htm?filter.iso3Language=eng' % page for page in range(1,pages_no+1)]

    x = pd.DataFrame(links, columns=['link'])
    x.to_csv('scrapy_links.csv',sep=",", index = False)
    
    
    class GetReviews(scrapy.Spider):
        name = 'reviews'
        allowed_domains = ['glassdoor.com']
        
        try:
            with open("scrapy_links.csv", "rt") as f: # get links from previous step
                start_urls = [url.strip() for url in f.readlines()][1:] # select rows that are not headers
        except:
            start_urls = [] 
        
        def parse(self, response):
            df_result_final = pd.DataFrame(columns=['Review_ID','Pros', 'Cons'])
            
            review_id_clean = []
            pros_clean = []
            cons_clean = []
            
            rev_xpath = '//span[@class="flagContent"]'
            pros_xpath = '//span[@data-test="pros"]//text()'
            cons_xpath = '//span[@data-test="cons"]//text()'
    
            rev_extract = response.xpath(rev_xpath)
            pros_extract = response.xpath(pros_xpath).getall()
            cons_extract = response.xpath(cons_xpath).getall()
            
            time.sleep(20) # set time sleeper after each page (to be polite)
            
            for x in rev_extract:
                y = x.get()[49:72]
                if y == None or y == "":
                    y_2 = 'null'
                else:
                    y_2 = y.split('"')[1]
                review_id_clean.append(y_2)
            df_rev = pd.DataFrame(review_id_clean, columns = ['Review_ID'])
           
            for xx in pros_extract:
                if xx == None or xx == "":
                    y1 = 'null'
                else:
                    y1 = str(xx).replace("\n", " ").replace("\r", " ").replace(";", " ") # replace semicolons with whitespaces so that it can be used later as delimiter
                pros_clean.append(y1)   
            df_x = pd.DataFrame(pros_clean, columns=['Pros'])    
            
            for zz in cons_extract:
                if zz == None or zz == "":
                    y2 = 'null'
                else:
                    y2 = str(zz).replace("\n", " ").replace("\r", " ").replace(";", " ") # replace semicolons with whitespaces so that it can be used later as delimiter
                cons_clean.append(y2)
            df_y = pd.DataFrame(cons_clean, columns=['Cons'])            
    
        
            df_xy = pd.concat([df_rev, df_x, df_y], axis=1)
            df_result_final = df_result_final.append(df_xy)
            
            # Save the result to csv with mode=append and header being added only during first iteration
            df_result_final.to_csv('output_glassdoor_scrapy.csv', sep=";", mode='a', header=not os.path.exists('output_glassdoor_scrapy.csv'), index = False)       
                    
else:
    links = []
    for y in itertools.count(start=1):
        url = 'https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036_P'+str(y)+'.htm?filter.iso3Language=eng'
        links.append(url)
        x = pd.DataFrame(links, columns=['link'])
        x.to_csv('scrapy_links.csv',sep=",", index = False)
    
        if y > 6802:
            break
        
        else:
    
            class GetReviews(scrapy.Spider):
                name = 'reviews'
                allowed_domains = ['glassdoor.com']
                
                try:
                    with open("scrapy_links.csv", "rt") as f: # get links from previous step
                        start_urls = [url.strip() for url in f.readlines()][1:] # select rows that are not headers
                except:
                    start_urls = [] 
                    
                
                def parse(self, response):
                    df_result_final = pd.DataFrame(columns=['Review_ID','Pros', 'Cons'])
                    
                    review_id_clean = []
                    pros_clean = []
                    cons_clean = []
                    
                    rev_xpath = '//span[@class="flagContent"]'
                    pros_xpath = '//span[@data-test="pros"]//text()'
                    cons_xpath = '//span[@data-test="cons"]//text()'
            
                    rev_extract = response.xpath(rev_xpath)
                    pros_extract = response.xpath(pros_xpath).getall()
                    cons_extract = response.xpath(cons_xpath).getall()
                    
                    time.sleep(20) # set time sleeper after each page (to be polite)
    
                    
                    for x in rev_extract:
                        y = x.get()[49:72]
                        if y == None or y == "":
                            y_2 = 'null'
                        else:
                            y_2 = y.split('"')[1]
                        review_id_clean.append(y_2)
                    df_rev = pd.DataFrame(review_id_clean, columns = ['Review_ID'])
                   
                    for xx in pros_extract:
                        if xx == None or xx == "":
                            y1 = 'null'
                        else:
                            y1 = str(xx).replace("\n", " ").replace("\r", " ").replace(";", " ") # replace semicolons with whitespaces so that it can be used later as delimiter
                        pros_clean.append(y1)   
                    df_x = pd.DataFrame(pros_clean, columns=['Pros'])    
                    
                    for zz in cons_extract:
                        if zz == None or zz == "":
                            y2 = 'null'
                        else:
                            y2 = str(zz).replace("\n", " ").replace("\r", " ").replace(";", " ") # replace semicolons with whitespaces so that it can be used later as delimiter
                        cons_clean.append(y2)
                    df_y = pd.DataFrame(cons_clean, columns=['Cons'])            
            
                
                    df_xy = pd.concat([df_rev, df_x, df_y], axis=1)
                    df_result_final = df_result_final.append(df_xy)
                    
                    # Save the result to csv with mode=append and header being added only during first iteration
                    df_result_final.to_csv('output_glassdoor_scrapy.csv', sep=";", mode='a', header=not os.path.exists('output_glassdoor_scrapy.csv'), index = False)       
                            
          