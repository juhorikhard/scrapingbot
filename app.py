from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def scrape_power(query):
    driver = webdriver.Firefox()
    # Searching from Power.fi with the keyword
    driver.get(f'https://www.power.fi/search/?q={query}')
    # Waiting for the site to load everything
    time.sleep(1)
    try:
        # Accepting cookies
        powerCookies = driver.find_element(By.CSS_SELECTOR, "button.coi-banner__accept:nth-child(3)")
        powerCookies.click()
        time.sleep(1)
        # Clicking the right item
        powerItem = driver.find_element(By.CSS_SELECTOR, "div.mb-spacer-mini:nth-child(4) > div:nth-child(1) > pwr-product-item-wrapper:nth-child(1) > div:nth-child(1) > div:nth-child(1) > pwr-product-item-v2:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > pwr-product-image:nth-child(1) > div:nth-child(1) > picture:nth-child(1) > img:nth-child(4)")
        powerItem.click()
        time.sleep(1)
        # Scraping the product name
        product_name = driver.find_element(By.CSS_SELECTOR, "h1.bold").text
        # Scraping the price
        price = driver.find_element(By.CSS_SELECTOR, ".p-spacer-xmini > pwr-price:nth-child(1)").text
    except Exception as e:
        print(f"Error: {e}")
        product_name = 'Not found'
        price = 'Not found'
    driver.quit()
    return product_name, price

def scrape_gigantti(query):
    driver = webdriver.Firefox()
    # Searching from Gigantti.fi with the keyword
    driver.get(f'https://www.gigantti.fi/search?q={query}')
    # Waiting for the site to load everything
    time.sleep(1)
    try:
        # Accepting cookies
        giganttiCookies = driver.find_element(By.CSS_SELECTOR, "button.coi-banner__accept:nth-child(3)")
        giganttiCookies.click()
        time.sleep(1)
        # Clicking the right item
        giganttiItem = driver.find_element(By.CSS_SELECTOR, "li.h-auto:nth-child(1) > a:nth-child(3)")
        giganttiItem.click()
        time.sleep(1)
        # Scraping the product name
        product_name = driver.find_element(By.CSS_SELECTOR, ".xl\:text-4xl").text
        # Scraping the price
        price = driver.find_element(By.CSS_SELECTOR,".xl\:p-8 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)").text
    except Exception as e:
        print(f"Error: {e}")
        product_name = 'Not found'
        price = 'Not found'
    driver.quit()
    return product_name, price

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    power_product, power_price = scrape_power(query)
    gigantti_product, gigantti_price = scrape_gigantti(query)
    return jsonify({
        'power': {'product': power_product, 'price': power_price},
        'gigantti': {'product': gigantti_product, 'price': gigantti_price}
    })

if __name__ == '__main__':
    app.run(debug=True)
