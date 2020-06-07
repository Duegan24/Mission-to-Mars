
# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def mars_news(browser):
    
    # Get Newest article title and teaser body
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Error Handling
    try:
        # Pull the first item from the unstructured list, list item
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    #Featured Image Download
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    # Error Handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    # Error Handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    # Assign column and set index of dataframe
    df.columns=['Description', 'Value']
    # df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, and bootstrap
    return df.to_html(index=False, classes='table-striped', justify='center')

def hemisphere_image(browser):
    #Featured Image Download
    # Set Variables
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_root = 'https://astrogeology.usgs.gov/'
    subsites = []
    hemispheres = []
    
    # Navigate to site will all the hemispere links
    browser.visit(url)
    # Convert the browser html to a soup object
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Error Handling
    try:
        # Find the information for each hemisphere
        products = img_soup.find_all('div', class_='item')

        # Go through the information for each hemisphere and pull out the url for the full res image
        for product in products:
            url_partial = product.find('a').get('href')
            url_subsite = url_root + url_partial
            subsites.append(url_subsite)

        # Go to each subsite and get the image url and title and append to a list
        for subsite in subsites:
            browser.visit(subsite)
            html = browser.html
            img_soup = BeautifulSoup(html, 'html.parser')
            # Use the parent element of downloads then find first 'a' tag and get the href to get image url
            img_url = img_soup.find("div", class_='downloads').select_one('a').get('href')
            # Use the parent element of content and then h2 tag to get title
            title = img_soup.find('div', class_='content').select_one('h2').get_text()
            # Append to Hemispheres List
            hemispheres.append({'title': title, 'img_url': img_url})


    except AttributeError:
        return None

    
    return hemispheres


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="C:/Users/jjgla/Documents/UT Austin Data Analytics Class/chromedriver.exe", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image(browser),
        "last_modified": dt.datetime.now()}

    browser.quit()

    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

