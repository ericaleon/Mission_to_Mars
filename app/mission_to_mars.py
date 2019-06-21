# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup

# set up and initialize browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News

# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Create BeautifulSoup object
soup = BeautifulSoup(browser.html, 'html.parser')

# find the 1st "slide" list element & 1st title "content title" div to retrieve article title
article_list = soup.find('li', class_='slide')
news_title = article_list.find('div', class_='content_title').get_text()
# news_title

# grab "article_teaser_body" as the paragraph text for the article
news_p = article_list.find('div', class_='article_teaser_body').get_text()
# news_p


# ### JPL Mars Images

# url of images page to be scraped
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)

# Create BeautifulSoup object
soup = BeautifulSoup(browser.html, 'html.parser')

# go to section with featured image
img_section = soup.find('div',class_ = "default floating_text_area ms-layer")    .footer.a
# print(img_section)

# grab relative url for "more info" data-link
detail_link = img_section["data-link"]

# create url to get to image detail page
img_url = f"https://www.jpl.nasa.gov{detail_link}"

# scrape image detail page
browser.visit(img_url)
img_soup = BeautifulSoup(browser.html, 'html.parser')

# get relative path of full size image
full_res_p = img_soup.find('figure', class_='lede').a
img_path = full_res_p.img["src"]

# add relative path to jpl base url for full size image url
featured_img_url = f"https://www.jpl.nasa.gov{img_path}"
# print(featured_img_url)


# ### Mars Weather

# go to URL to be scraped
w_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(w_url)

# Create BeautifulSoup object
w_soup = BeautifulSoup(browser.html, 'html.parser')

# find first tweet and get text
mars_weather = w_soup.find('div', class_="js-tweet-text-container").p.text
# print(mars_weather)


# ### Mars Facts

import pandas as pd

# Use pandas to read html and create a dataframe, then clean up df
facts_df = pd.read_html('https://space-facts.com/mars/')[0]
facts_df.columns = ['description', 'value']
facts_df.set_index('description', inplace=True)
# facts_df

# convert df to html table string
facts_df.to_html()


# ### Mars Hemispheres

# URL to be scraped using splinter
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)

# set up list that will include each hemisphere
hemisphere_img_urls = []

# Get list of elements containing links for hemispheres
links = browser.find_by_css("a.product-item h3")

# Loop through the links and click into them for img element info
for link in range(len(links)):
    hem = {}
    
    # click into a href element
    browser.find_by_css("a.product-item h3")[link].click()
    
    # from new page, find url & title associated with text "Sample"
    img_elem = browser.find_link_by_text('Sample')
    hem['img_url'] = img_elem['href']
    
    hem['title'] = browser.find_by_css("h2.title").text
    
    # add 'hem' dictionary to list
    hemisphere_img_urls.append(hem)
    
    # back to previous page
    browser.back()

# print(hemisphere_img_urls)



