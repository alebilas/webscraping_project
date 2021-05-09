# Glassdoor scrape
## _With use of BeaufitulSoup, Scrapy and Selenium libraries_

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries:
```bash
pip install pandas, beautifulsoup4, urllib, scrapy, selenium
```
## Usage
First, log in to [Glassdoor](https://www.glassdoor.com/index.htm), because the first 2 scripts will not fully work without it (the website has limitations in terms of unknown users activity).
Please use below credentials:

login: ab.jb.webscraping@gmail.com
password: webscraping2021

Note: Credentials were generated only for purpose of this project
Note2: The drive needs to be changed inside the Selenium script.

#### Start
-----
In terminal go to location where the code is stored, e.g.:
```bash
cd .\Desktop\webscraping
```
#### BeautifulSoup
-----
In terminal go to location where the BS project script is saved, e.g. cd .\soup (after running the above code). Then execute:
```bash
python3 .\scrape_bs.py
```
#### Scrapy
-----
In terminal go to location where the BS project script is saved, e.g. cd .\scrapy (after running the first code). Then execute:
```bash
scrapy runspider .\scrape_scrapy.py
```
#### Selenium
-----
In terminal go to location where the BS project script is saved, e.g. cd .\selenium (after running the first code). Then execute:
```bash
python3 .\scrape_selenium.py
```
