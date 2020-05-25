from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from bs4 import BeautifulSoup
import requests
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os

# Create your views here.

def contact(request):

    form = ContactForm()

    return render(request, 'index.html', {'form': form, })

def output(request):

    title = ""
    prixez = ""
    converted_price = ""
    name = ''
    url_amazon = ""
    url_ldlc = ""
    url_maxgaming = ""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['item']

    class AmazonBot(object):
        """Parses relevant information from a text file consisting of
        Amazon links."""

        def __init__(self, items):
            """Setup bot for Amazon URL."""
            self.amazon_url = "https://www.google.com/"
            self.items = items

            self.profile = webdriver.FirefoxProfile()
            self.options = Options()
            self.options.add_argument("--headless")
            self.options.add_argument("")
            self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                            firefox_options=self.options)

            # Navigate to the Amazon URL.
            self.driver.get(self.amazon_url)

            # Gets the source
            self.html = self.driver.page_source
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.html = self.soup.prettify('utf-8')

        def search_items(self):
            """Searches through the list of items and
            obtains name, price, and URL information for each item."""

            for item in self.items:
                print(f"Searching on Amazon for {item}...")

                self.driver.get(self.amazon_url)

                search = self.driver.find_element_by_name("q")
                time.sleep(2)

                search.send_keys(name + " amazon fr" + Keys.ENTER)
                time.sleep(2)

                amazon_link = self.driver.find_element_by_class_name("LC20lb")
                amazon_link.click()

                time.sleep(2)

                URL = self.driver.current_url

                headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}

                page = requests.get(URL, headers=headers)

                soup = BeautifulSoup(page.content, 'html.parser')

                try:
                    title = soup.find(id="productTitle").get_text()
                except Exception:
                    print("couldn\'t get title")
                try:
                    prixez = soup.find(id="priceblock_ourprice").get_text()
                except Exception:
                    print('price htmltag couldn\'t be found')
                global converted_price_amazon
                try:
                    converted_price_amazon = prixez[0:6].replace('\xa0', '').replace(",", ".")
                    url_item_amazon = self.driver.current_url
                    nonlocal url_amazon
                    url_amazon = url_item_amazon
                    print(url_amazon)
                except Exception:
                    print('converted_price can\'t be converted because it couldn\'t be found ')
                    converted_price_amazon = "amazon price not found"
                    url_item_amazon = "url not retrieved"
                    url_amazon = "no link found"
                try:
                    amazon_output = "amazon price: " + converted_price_amazon
                except Exception:
                    print('Amazon product has been found, but no price was displayed on the page')

                try:
                    print(title.strip() + "\n")
                except Exception:
                    print("no title")
                try:
                    print(amazon_output)
                except Exception:
                    print('looking for the next site to compare your product')


    items = [name]
    amazon_bot = AmazonBot(items)
    amazon_bot.search_items()
    os.system("taskkill /f /im geckodriver.exe /T")


    class LDLCBot(object):
        """Parses relevant information from a text file consisting of
        LDLC links."""

        def __init__(self, items):
            """Setup bot for LDLC URL."""
            self.amazon_url = "https://www.google.com/"
            self.items = items

            self.profile = webdriver.FirefoxProfile()
            self.options = Options()
            self.options.add_argument("--headless")
            self.options.add_argument("")
            self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                            firefox_options=self.options)

            # Navigate to the Amazon URL.
            self.driver.get(self.amazon_url)

            # Gets the source
            self.html = self.driver.page_source
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.html = self.soup.prettify('utf-8')

        def search_items(self):
            """Searches through the list of items and
            obtains name, price, and URL information for each item."""

            for item in self.items:
                print(f"Searching on LDLC for {item}...")

                self.driver.get(self.amazon_url)

                search = self.driver.find_element_by_name("q")
                time.sleep(2)

                search.send_keys("ldlc " + name + Keys.ENTER)
                time.sleep(2)

                amazon_link = self.driver.find_element_by_class_name("LC20lb")
                amazon_link.click()

                time.sleep(2)

                URL = self.driver.current_url

                headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}

                page = requests.get(URL, headers=headers)

                soup = BeautifulSoup(page.content, 'html.parser')

                try:
                    title = soup.find("h1", {"class": "title-1"}).get_text()
                    prixez = soup.find_all('div', {'class': 'price'})
                    # find page's item price(turns out [4] is the right price for the item you are looking at when loading the product page)
                    prixez = prixez[4]
                    global converted_price_ldlc
                    converted_price_ldlc = prixez
                    converted_price_ldlc = converted_price_ldlc.text.replace("€", ".")

                    print(title.strip() + "\n")
                    print("LDLC price: " + converted_price_ldlc)
                    url_item_ldlc = self.driver.current_url
                    nonlocal url_ldlc
                    url_ldlc = url_item_ldlc
                    print(url_ldlc)
                except Exception:
                    print("LDLC item couldn\'t be found, looking for the next item to compare")
                    converted_price_ldlc = "LDLC price not found"
                    url_item_ldlc = "url not retrieved"
                    url_ldlc = "no link found"


    items = [name]
    amazon_bot = LDLCBot(items)
    amazon_bot.search_items()
    os.system("taskkill /f /im geckodriver.exe /T")


    class MaxgamingBot(object):
        """Parses relevant information from a text file consisting of
        LDLC links."""

        def __init__(self, items):
            """Setup bot for LDLC URL."""
            self.amazon_url = "https://www.google.com/"
            self.items = items

            self.profile = webdriver.FirefoxProfile()
            self.options = Options()
            self.options.add_argument("--headless")
            self.options.add_argument("")
            self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                            firefox_options=self.options)

            # Navigate to the Amazon URL.
            self.driver.get(self.amazon_url)

            # Gets the source
            self.html = self.driver.page_source
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.html = self.soup.prettify('utf-8')

        def search_items(self):
            """Searches through the list of items and
            obtains name, price, and URL information for each item."""

            for item in self.items:
                print(f"Searching on Maxgaming for {item}...")

                self.driver.get(self.amazon_url)

                search = self.driver.find_element_by_name("q")
                time.sleep(2)

                search.send_keys("maxgaming " + name + Keys.ENTER)
                time.sleep(2)

                amazon_link = self.driver.find_element_by_class_name("LC20lb")
                amazon_link.click()

                time.sleep(2)

                URL = self.driver.current_url

                headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}

                page = requests.get(URL, headers=headers)

                soup = BeautifulSoup(page.content, 'html.parser')

                # title = soup.find("h1", {"class": "title-1"}).get_text()
                try:
                    prixez = soup.find_all('div', {'class': 'price'})

                    # if url contains us site url OR eu site url, get the right array index (as array indexes aren't the same based on how the site was coded, depending of the website region)
                    global converted_price_maxgaming
                    if "us.maxgaming.com" in URL:
                        prixez = prixez[18].text
                        converted_price_maxgaming = prixez[2:8]
                    elif "www.maxgaming.com" in URL:
                        prixez = prixez[21].text
                        converted_price_maxgaming = prixez[0:6]
                    # ldlc_output = converted_price

                    # print(title.strip() + "\n")
                    print("Maxgaming price: " + converted_price_maxgaming.strip().replace(".", ","))
                    url_item_maxgaming = self.driver.current_url
                    nonlocal url_maxgaming
                    url_maxgaming = url_item_maxgaming
                    print(url_maxgaming)

                except Exception:
                    print("Maxgaming item couldn\'t be found, code execution will continue..")
                    converted_price_maxgaming = "MaxGaming price not found"
                    url_maxgaming = "no link found"


    items = [name]
    amazon_bot = MaxgamingBot(items)
    amazon_bot.search_items()
    os.system("taskkill /f /im geckodriver.exe /T")

    arr = []
    try:
        print("Amazon price: " + converted_price_amazon)
    except Exception:
        print("amazon price not found")
    else:
        arr.append(converted_price_amazon)

    try:
        print("LDLC price: " + converted_price_ldlc)
    except Exception:
        print("LDLC price not found")
    else:
        arr.append(converted_price_ldlc)

    try:
        print("Maxgaming price: " + converted_price_maxgaming.strip())
    except Exception:
        print("Maxgaming price not found")
    else:
        arr.append(converted_price_maxgaming)

    arr.sort()
    result = ''
    if not arr:
        converted_price = ''
        result = "No result for " + name + " has been found"
    else:
        converted_price = arr[0]

    try:
        if arr[0] == converted_price_amazon:
            print("According to us, you should consider buying " + name + " from Amazon")
            result = "According to us, you should consider buying " + name + " from Amazon"
    except Exception:
        print("")

    try:
        if arr[0] == converted_price_ldlc:
            print("According to us, you should consider buying " + name + " from LDLC")
            result = "According to us, you should consider buying "  + name +  " from ldlc"
    except Exception:
        print("")

    try:
        if arr[0] == converted_price_maxgaming:
            print("According to us, you should consider buying " + name + " from MaxGaming")
            result = "According to us, you should consider buying "  + name +  " from MaxGaming"
    except Exception:
        print("")



    return render(request, 'output.html', {'converted_price': converted_price, 'result': result, 'converted_price_amazon': converted_price_amazon, 'converted_price_ldlc': converted_price_ldlc, 'converted_price_maxgaming': converted_price_maxgaming, 'url_amazon': url_amazon, 'url_ldlc': url_ldlc, 'url_maxgaming': url_maxgaming})
