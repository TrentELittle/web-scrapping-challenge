# Import dependencies
import os
import sys
from multiprocessing import Process
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pprint
import pandas as pd



""" create path for browser when scraping Nasa's site"""
# Note: Replace the path with your own path to the chromedriver
        
executable_path = {'executable_path': 'C:/chromedriver'}
browser = Browser("chrome", **executable_path, headless=False)


def headline(browser):
    """Scraping top headline of Nasa Mars News"""

    #Run browser and visit Nasa Mars News site
    # browser = init_browser()
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # Variables for browser initialization and cleaning data through bs
    html = browser.html
    soup = bs(html, "html.parser")

    # Create path to pull title and summary of top headline
    content_path = soup.find("div", class_= "list_text")

    news_title = content_path.find("div", class_ = "content_title").get_text()
    news_p = content_path.find("div", class_ = "article_teaser_body").get_text()

    #Print title and summary
    output = print(f'Title: {news_title}', 
                   f'\nSummary: {news_p}')

    # browser.quit()

    return news_title, news_p

def featured_image(browser):
    """Scraping featured image from JPL Mars Space Images"""


    #Run Browser and visit JPL(jet propultion laboratory) site
    jpl_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Variables for browser init and cleaning data through bs
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "html.parser")

    # Find the featured image url from jpl_url
    featured_image_url = jpl_soup.find('div', class_ = "carousel_container").article.footer.a["data-fancybox-href"]
    featured_image_url = f"https://jpl.nasa.gov/spaceimages{featured_image_url}"

    # Print the url for the image
    output = print(f"featured_image_url = {featured_image_url}")

    # browser.quit()

    return featured_image_url


def mars_info():
    """Scraping Mars Facts webpage for planet info"""

    # Create path for mars facts url and use pandas to read the url into HTML table string
    mfacts_url = "https://space-facts.com/mars/"
    planet_profile = pd.read_html(mfacts_url)
    planet_profile

    # read only mars data 
    mars_table = planet_profile[0]
    output = print(mars_table)
    # browser.quit()

    return mars_table

def hemispheres(browser): 
    """Obtain high res images for each of Mar's hemispheres from USGS Astrogeology site"""

    # Path to USGS Astrogeology site and open in browser
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    # Variables for browser init and cleaning data through bs
    usgs_html = browser.html
    usgs_soup = bs(usgs_html, "html.parser")

    # Create empty list for hemisphere photos
    hemisphere_image_urls = []

    # Create a loop to append title and image url into empty list from the images
    images = usgs_soup.find_all("div", class_ = "item")

    for image in images:
        # Create dictionary to house each link and title individually before appending to list
        hemisphere_info = {}
        
        # title
        hemisphere_info["title"] = image.find("h3").text
        
        # follow individual link to full size image
        img_src = image.find("a")["href"]
        img_link = f"https://astrogeology.usgs.gov{img_src}"
        browser.visit(img_link)
        img_html = browser.html
        img_soup = bs(img_html, "html.parser")
        
        # image url
        img_url = img_soup.find("div", class_ = "downloads").a["href"]
        hemisphere_info["img_url"] = img_url
        
        # append info to hemisphere_image_urls
        hemisphere_image_urls.append(hemisphere_info)
    pp = pprint.PrettyPrinter(indent = 4)
    hemispheres = pp.pprint(hemisphere_image_urls)

    browser.quit()

    return hemispheres_image_urls

def scrape():
    executable_path = {'executable_path': 'C:/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = headline(browser)
    featured_image_url = featured_image(browser)
    mars_info = mars_info()
    hemisphere_image_urls = hemispheres(browser)

    data = {"News Title": news_title,
            "News Paragraph": news_p,
            "Featured Image": featured_image_url,
            "Mars Facts": mars_info,
            "Hemisphere Photos": hemisphere_image_urls
            }
    
    browser.quit()
    return data



if __name__ == "__main__":
    # headline()
    # featured_image()
    # mars_info()
    # hemispheres()
    print(scrape_all())