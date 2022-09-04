# Scrip resources:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-using-tag-names 
# https://stackoverflow.com/questions/53965295/selenium-beautifulsoup-python-loop-through-multiple-pages

# Library Section
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

#%% Code to start the browser
driver = webdriver.Chrome()
driver.get('https://www.kohls.com/catalog/mens-button-down-shirts-tops-clothing.jsp?CN=Gender:Mens+Silhouette:Button-Down%20Shirts+Category:Tops+Department:Clothing&cc=mens-TN3.0-S-buttondownshirts&kls_sbp=43160314801019132980443403449632772558&PPP=120&WS=0')

#%% Create Global Variables
products = []
hyperlinks = []
reviewCounts = []
starRatings = []

pageCounter = 0

#%% Loop through page reviews
html_soup = BeautifulSoup(driver.page_source, 'html.parser')
maxPageCount = int(html_soup.find('input', class_ = 'pageNum pageInput').text)+1

prod_containers = html_soup.find_all('li', class_ = 'products_grid')


while (pageCounter < maxPageCount):
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    prod_containers = html_soup.find_all('li', class_ = 'products_grid')
    for product in prod_containers:
        # If the product has review count, then extract:
        if product.find('span', class_ = 'prod_ratingCount') is not None:
            # The product name
            name = product.find('div', class_ = 'prod_nameBlock')
            name = re.sub(r"\s+", " ", name.text)
            name = name.strip()
            products.append(name)

            # The product hyperlink
            hyperlink = product.find('span', class_ = 'prod_ratingCount')
            hyperlink = hyperlink.a
            hyperlink = hyperlink.get('href')
            hyperlinks.append(hyperlink)

            # The product review count
            reviewCount = product.find('span', class_ = 'prod_ratingCount').a.text
            reviewCounts.append(reviewCount)

            # The product overall star ratings
            starRating = product.find('span', class_ = 'prod_ratingCount')
            starRating = starRating.a
            starRating = starRating.get('alt')
            starRatings.append(starRating) 

    driver.find_element_by_xpath('//*[@id="page-navigation-top"]/a[2]').click()
    pageCounter +=1
    print(pageCounter)

