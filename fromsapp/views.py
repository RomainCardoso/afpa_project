from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm, HiddenForm
from bs4 import BeautifulSoup
import sys, time, os, requests, string
from selenium import webdriver
from django.contrib.auth.decorators import login_required
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from .models import Search, Favorite
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


def contact(request):

    form = ContactForm()

    return render(request, 'fromsapp/index.html', {'form': form, })

@login_required
def output(request):

    title = ""
    prixez = ""
    converted_price = ""
    name = ''
    name_convert = ''
    url_amazon = ""
    url_ldlc = ""
    url_maxgaming = ""
    item_image = ''
    descriptions = ''
    carousel = []

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
            self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                            firefox_options=self.options)

            # Navigate to the Amazon URL.
            self.driver.get(self.amazon_url)

            # Gets the source
            self.lxml = self.driver.page_source
            self.soup = BeautifulSoup(self.lxml, 'lxml')
            self.lxml = self.soup.prettify('utf-8')

        def search_items(self):
            """Searches through the list of items and
            obtains name, price, and URL information for each item."""

            for item in self.items:
                print(f"Searching on Amazon for {item}...")

                self.driver.get(self.amazon_url)

                search = self.driver.find_element_by_name("q")
                time.sleep(2)

                search.send_keys(name + " amazon.fr" + Keys.ENTER)
                time.sleep(2)

                amazon_link = self.driver.find_element_by_class_name("LC20lb")
                amazon_link.click()

                time.sleep(2)

                URL = self.driver.current_url

                headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}

                page = requests.get(URL, headers=headers)

                soup = BeautifulSoup(page.content, 'lxml')



                try:
                    images = soup.find(id='landingImage')
                    nonlocal item_image
                    item_image = images['src']
                    print(item_image)
                    print("\n yep .. that's the image")
                except Exception:
                    print('no image found')

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
                # time.sleep(2)

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
                    nonlocal item_image
                    if item_image == '':
                        image = soup.find(id='ctl00_cphMainContent_ImgProduct')
                        item_image = image['src']
                except Exception:
                    print('')

                try:
                    images = soup.find_all('img')
                    product_img = []
                    for image in images:
                        product_img.append(image['src'])
                    count = 14
                    while count <= 18:
                        nonlocal carousel
                        carousel.append(product_img[count])
                        count += 1
                    print(carousel)
                except Exception:
                    print('empty carousel')

                try:
                    nonlocal descriptions
                    if descriptions == '':
                        descriptions = soup.find(class_='desc').get_text()
                except Exception:
                    print('Description not found')
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
                # time.sleep(2)

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

                    # if url contains us site url OR eu site url, get the right array index (as array indexes aren't the same based on how the site was coded, depending of the website's region)
                    global converted_price_maxgaming
                    if "us.maxgaming.com" in URL:
                        prixez = prixez[18].text
                        converted_price_maxgaming = prixez[2:8]
                    elif "www.maxgaming.com" in URL:
                        prixez = prixez[21].text
                        converted_price_maxgaming = prixez[0:6]
                    elif "www.maxgaming.fi" in URL:
                        prixez = prixez[21].text
                        converted_price_maxgaming = prixez[0:6]


                    print("Maxgaming price: " + converted_price_maxgaming.strip())
                    if "www.maxgaming.fi" in URL and converted_price_maxgaming:
                        converted_price_maxgaming = converted_price_maxgaming.strip().replace(",", ".")
                    url_item_maxgaming = self.driver.current_url
                    nonlocal url_maxgaming
                    url_maxgaming = url_item_maxgaming
                    print(url_maxgaming)
                    if "www.maxgaming.com/" in url_maxgaming:
                        print("acces to link has been granted !")
                    elif "us.maxgaming.com/" in url_maxgaming:
                        print("acces to link has been granted !")
                    elif "www.maxgaming.fi" in url_maxgaming:
                        print("acces to link has been granted !")
                    else:
                        print('acces to link has been blocked !')
                        converted_price_maxgaming = "MaxGaming price not found"

                except Exception:
                    print("Maxgaming item couldn\'t be found, code execution will continue..")
                    converted_price_maxgaming = "MaxGaming price not found"
                    url_maxgaming = "no link found"

    items = [name]
    amazon_bot = MaxgamingBot(items)
    amazon_bot.search_items()
    os.system("taskkill /f /im geckodriver.exe /T")
    name_convert = string.capwords(name)

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

    #Get connected user
    user = request.user

    #Create hidden form for favorites
    form_fav = HiddenForm(initial = {'name' : name, 'amazon_url': url_amazon, 'ldlc_url': url_ldlc, 'maxgaming_url': url_maxgaming, 'amazon_price': converted_price_amazon, 'ldlc_price': converted_price_ldlc, 'maxgaming_price': converted_price_maxgaming, 'search_user': user})

    #Query to store search in db
    search = Search(searched_item = name, amazon_url = url_amazon, ldlc_url = url_ldlc, maxgaming_url = url_maxgaming, amazon_price = converted_price_amazon, ldlc_price = converted_price_ldlc, maxgaming_price = converted_price_maxgaming, search_user = user)
    search.save()

    args = {
        'item_image': item_image,
        'carousel': carousel,
        'name_convert': name_convert,
        'descriptions': descriptions,
        'converted_price': converted_price,
        'result': result,
        'converted_price_amazon': converted_price_amazon,
        'converted_price_ldlc': converted_price_ldlc,
        'converted_price_maxgaming': converted_price_maxgaming,
        'url_amazon': url_amazon,
        'url_ldlc': url_ldlc,
        'url_maxgaming': url_maxgaming,
        'form': form_fav,
    }

    return render(request, 'fromsapp/output.html', args)

@user_passes_test(lambda u: u.is_superuser)
def history(request):
    context = {
        'searchs' : Search.objects.all()
    }
    return render(request, 'fromsapp/history.html', context)

#Add fav to DB
@login_required
def favorites(request):
    user = request.user
    if request.method == 'POST':
        form = HiddenForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            amazon_price = form.cleaned_data.get('amazon_price')
            ldlc_price = form.cleaned_data.get('ldlc_price')
            maxgaming_price = form.cleaned_data.get('maxgaming_price')
            amazon_url = form.cleaned_data.get('amazon_url')
            ldlc_url = form.cleaned_data.get('ldlc_url')
            maxgaming_url = form.cleaned_data.get('maxgaming_url')
            added_favorite = Favorite(name=name, amazon_price=amazon_price, ldlc_price=ldlc_price, maxgaming_price=maxgaming_price, amazon_url=amazon_url, ldlc_url=ldlc_url, maxgaming_url=maxgaming_url, search_user=user)
            added_favorite.save()

    args = {
        'favorites' : user.favorite_set.all(),
    }

    return render(request, 'fromsapp/favorites.html', args)
