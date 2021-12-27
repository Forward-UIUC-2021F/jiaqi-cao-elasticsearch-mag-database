from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import time

options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)

""" 
uses webdriver object to execute javascript code and get head of the document 
url: url of the page
driver: web driver used
head: if True then return the head element of the page, else return the body
"""
def get_soup(url, driver, head = True):
    driver.get(url)
    res_html = driver.execute_script('return document.{}.innerHTML'.format("head" if head else "body"))

    # beautiful soup object to be used for parsing html content
    soup = BeautifulSoup(res_html,'html.parser') 
    return soup

""" 
query: acronym of institution to be searched
driver: web driver used

return: a list of institutions that the query might refer to
"""
def scrape_institution_page(query, driver):
    # generate the wikipedia page based on query
    link = "https://en.wikipedia.org/wiki/" + re.sub("\s+", r'_', query)

    soup = get_soup(link,driver)
    print("Searching for url: ", link)
   
    # Get rid of " - Wikipeida" in the title
    title = soup.title.string[:-12]
    print("The page's title is", title)

    # case 1: the page is automatically redirected to the institution's main page given the acronym
    # e.g. UIUC; UCLA
    if title.lower() != query.lower():
        return [title]
    
    soup = get_soup(link, driver, head = False)
    content = soup.find(id = "mw-content-text")
    institutions = []

    # first p element in the page, determines whether the page has a "most often refers to section"
    main_div = content.div
    first_p = main_div.p 
    current_elem = first_p.find_next_sibling()

    # case 2: the aconym have one or more "most often refers to" institution, these will be returned
    # e.g. USC; CMU
    if current_elem.name == "ul":
        
        # get all "most often refers to" institution
        for element in current_elem:
            a = element.find("a")
            if a != -1:
                institutions.append(a.string)

    # case 3: the institutions are in the "education" or "universities" section
    # e.g. UW; UCB
    else:

        # find the header to which the section of "education" or "universities" follows
        headers = main_div.find_all("h2")
        
        for header in headers:
            if header.span:
                if header.span.string:
                    if "education" in header.span.string.lower() or "universities" in header.span.string.lower():
                        current_elem = header
        
        # go to the next sibling of the header and gather all names of institutions here
        current_elem = current_elem.find_next_sibling()

        # this loop is to prevent the case where the program stops when reaching a h3 header
        while current_elem.name != "h2" :
            if current_elem.name == "ul":
                for element in current_elem:
                    a = element.find("a")
                    if a != -1:
                        institutions.append(a.string)

            current_elem = current_elem.find_next_sibling()

    return institutions

# tests
for query in ["uiuc", "usc", "cmu", "ucb", "uw"]:
    print(scrape_institution_page(query, driver))
