from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

#Set up the chromedriver path
def init_browser():
        executable_path = {'executable_path': 'C:\chromedrv\chromedriver.exe'}
        return Browser('chrome', **executable_path, headless=False)

def scrape():
        browser = init_browser()

#JPL Scraping (1)
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        time.sleep(10)
        html = browser.html
        soup = bs(html, 'html.parser')

        #button = soup.find('footer', class_='button fancybox')
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(10)
        #All Praise The Jeff
        thingy = soup.find(class_='carousel_item')['style']
        nurl = thingy.split("'")[1]
        featured_image_url = 'https://www.jpl.nasa.gov' + nurl

        print(featured_image_url)

        #News Scraping (2)
        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        response = requests.get(url)
        time.sleep(10)
        soup = bs(response.text, 'lxml')

        news_title = soup.find(class_='content_title').text
        print(news_title)

        # Retrieve the paragraph text
        news_p = soup.find(class_='rollover_description_inner').text
        print(news_p)

        #Twitterness (3)
        twitter_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(twitter_url)

        time.sleep(10)
        html = browser.html
        soup = bs(html, "html.parser")
        mars_weather = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        print(mars_weather)
        
        #Space Facts Scraping (4)
        facts_url = 'https://space-facts.com/mars/'
        browser.visit(facts_url)

        time.sleep(10)

        tables = pd.read_html(facts_url)

        #Create scraped table into dataframe
        df = tables[0]
        df.columns = ['','']
        html_table = df.to_html()

        print(html_table)

        #USGS Image Scraping (5)
        browser = init_browser()

        hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        hemi_list = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
        hemisphere_image_urls = []
        browser.visit(hemi_url)
        time.sleep(10)

        for hemi in hemi_list:
            browser.click_link_by_partial_text(hemi)
            time.sleep(10)
            hemi_html = browser.html
            hemi_soup = bs(hemi_html, 'html.parser')
            url = hemi_soup.find('div', class_='downloads').ul.li.a['href']
            name = hemi_soup.title.text.partition(' Enhanced')[0]
            hemisphere_image_urls.append({'title':name, 'img_url':url})
            time.sleep(10)
            browser.back()


        # Store data in a dictionary
        mars_data = {
        "JPL_featured_img": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": html_table,
        "Cerberus": Cerberus,
        "Schiaparelli": Schiaparelli,
        "Syrtis": Syrtis,
        "Valles": Valles,
        "News_Title": news_title,
        "News_p": news_p,
        }

        # Close the browser after scraping
        browser.quit()

        return mars_data

if __name__ == '__main__':
    scrape()