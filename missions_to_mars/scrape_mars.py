#!/usr/bin/env python
# coding: utf-8
# import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pandas as pd
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

def scrape():
    # empty dictionary to store all values in
    mars = {}

    # # NASA Mars News
    # URL of MARS NEWS page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # SELENIUM
    driver = webdriver.Chrome()
    response = driver.get(url)
    soup = bs(driver.page_source, "html.parser")
    driver.quit()

    # find title and paragraph
    title = soup.find('div', class_='content_title')
    mars['title']=title.text
    #print(title.text)

    paragraph = soup.find('div', class_='article_teaser_body')
    #paragraph = paragraph.get_text()
    mars['paragraph'] = paragraph
    #print(mars)


    # # JPL Mars Space Images - Featured Image
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    image = soup.find('a', class_="button fancybox")
    image_url = image['data-fancybox-href']
    firstparturl = 'https://www.jpl.nasa.gov/'
    mars['featured_image_url'] = firstparturl + image_url
    #print(mars)
    browser.quit()


    # # Mars Weather
    # URL of MARS WEATHER page to be scraped
    url = "https://twitter.com/marswxreport?lang=en"

    # retrieve page with requests module
    response = requests.get(url)

    # create Beautiful Soup object and parse
    soup = bs(response.text, 'lxml')
    #print(soup.prettify())

    # scrape latest weather tweet
    mars_weather = soup.find('p', class_='TweetTextSize')
    mars['mars_weather'] = mars_weather.text
    #print(mars)

    # # Mars Facts
    # save url of MARS FACTS webpage
    url = 'https://space-facts.com/mars/'
    # extract tables from website
    tables = pd.read_html(url)

    # create df
    mars_df = tables[0]
    mars_df.columns=['Category','MARS']

    # convert df to html table string 
    mars_html = mars_df.to_html()
    mars['mars_html'] = mars_html.replace('\n','')
    #print(mars)

    # save html to file and hide index
    mars_df.to_html('mars_facts.html', index=False)
    #get_ipython().system('open mars_facts.html')

    # # Mars Hemispheres
    # SELENIUM
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver = webdriver.Chrome()
    response = driver.get(url)
    soup = bs(driver.page_source, "html.parser")
    hemisphere_image_urls = []
    y = 0

    # print title of each hemisphere in for loop
    for each in list(soup.find_all('div', class_='item')):
        title = each.find('h3').text
        
        for x in range(4):
            x += y
            driver.find_element_by_xpath(f'//*[@id="product-section"]/div[2]/div[{x+1}]/a/img').click()    
            driver.find_element_by_xpath('//*[@id="wide-image-toggle"]').click()

            # print urls
            img = driver.find_element_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')
            img_url = img.get_attribute('href')

            hemispheres = {"title": title, "img_url": img_url}
            hemisphere_image_urls.append(hemispheres)
            break
            
        driver.back()
        y += 1    

    mars['hemisphere_image_urls']=hemisphere_image_urls
    #print(mars)
    driver.quit()

    return mars