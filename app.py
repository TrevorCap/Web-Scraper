from flask import Flask, render_template, redirect, Markup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from flask_pymongo import PyMongo
import pandas as pd
import time


def splintering():
    executable_path = {'executable_path': 'C:\ChromeDriver\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def souping():
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def flasking():
    app =Flask(__name__)
    return app

def mongoing():
    mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")
    return mongo

def newsing():
    browser = splintering()
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    time.sleep(.25)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news1 = soup.select_one('ul.item_list li.slide')
    head1 = news1.find('div', class_='bottom_gradient').get_text()
    body1 = news1.find('div', class_='article_teaser_body').get_text()
    browser.quit()
    return head1, body1

def imaging():
    browser = splintering()
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(1)
    clicker1 = browser.find_link_by_partial_text('FULL IMAGE')
    clicker1.click()
    time.sleep(2)
    clicker1 = browser.find_link_by_partial_text('more info')
    clicker1.click()
    time.sleep(1)
    html2 = browser.html
    soupy = BeautifulSoup(html2, 'html.parser')
    url3 = soupy.select_one('figure.lede a img').get('src')
    url4 = f'https://www.jpl.nasa.gov{url3}'
    browser.quit()
    return url4

def tweeting():
    browser = splintering()
    url5 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url5)
    time.sleep(1)
    html3 = browser.html
    soupiest = BeautifulSoup(html3, 'html.parser')
    tweet = soupiest.find('div',class_='js-tweet-text-container')
    weather = tweet.find('p').text.strip()
    link =  tweet.find('p').find('a').text.strip()
    weather = weather.replace(link, '')
    tweet = weather.replace('\n', '')
    browser.quit()
    return tweet

def facting():
    url6 = 'http://space-facts.com/mars/'
    table = pd.read_html(url6)
    table = table[0]
    table.columns = ['Fact', 'Figure']
    table = table.to_html(index=False)
    return table

def hurling():
    browser = splintering()
    url7 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url7)
    html4 = browser.html
    soupiester = BeautifulSoup(html4, 'html.parser')
    ilinks = browser.find_by_css('a.product-item h3')
    hurls = []
    for x in range(len(ilinks)):
        time.sleep(1)
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[x].click()
        sample = browser.find_link_by_text('Sample').first
        hemisphere['iurl'] = sample['href']
        hemisphere['Title'] = browser.find_by_css('h2.title').text
        hurls.append(hemisphere)
        browser.back()
    browser.quit()
    return hurls

def scrapeitall():
    mongo = mongoing()
    table = facting()
    url4 = imaging()
    tweet = tweeting()
    head1, body1 = newsing()
    hurls = hurling()
    dictionary = {'url4': url4, 'tweet': tweet, 'head1': head1, 'body1': body1, 'hemisphere': hurls, 'table': table}
    return dictionary


app = flasking()
mongo = mongoing()

@app.route('/')
def home():
    dictionary = mongo.db.collection.find_one()
    return render_template("index.html", data=dictionary)

@app.route('/scrape')
def scrape():
    dictionary = scrapeitall()
    mongo.db.collection.replace_one({}, dictionary, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)