import requests
from bs4 import BeautifulSoup
import psycopg2
import json
import socks
import socket
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

# Set up Tor proxy for Selenium
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': '127.0.0.1:9050',
    'ftpProxy': '127.0.0.1:9050',
    'sslProxy': '127.0.0.1:9050',
})

# Set up Firefox options
options = FirefoxOptions()
options.headless = True

# Route traffic through Tor for requests
SOCKS_PORT = 9050  # Default Tor SOCKS port
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", SOCKS_PORT)
socket.socket = socks.socksocket

# Establish connection to your database
try:
    con = psycopg2.connect(
        host = "your_host", 
        database="your_database", 
        user = "your_username", 
        password = "your_password")
except psycopg2.Error as e:
    print(f"Could not make a connection to the database. Error: {e}")
    exit()

cur = con.cursor()

# Function to create necessary tables
def create_tables():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id SERIAL PRIMARY KEY,
        url TEXT NOT NULL
    )
    ''')
    con.commit()

# Function to get URLs using requests
def get_urls_with_requests(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a', href=True)]
        return urls
    except Exception as e:
        print(f"Error getting URLs with requests: {e}")
        return []

# Function to get URLs using Selenium
def get_urls_with_selenium(url):
    try:
        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox(options=options, proxy=proxy)

        # Visit the URL
        driver.get(url)

        # Wait for the dynamic content to load
        time.sleep(3)

        # Pass the page source to BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all 'a' tags with 'href' attributes
        urls = [link.get('href') for link in soup.find_all('a', href=True)]

        driver.quit()
        return urls
    except Exception as e:
        print(f"Error getting URLs with Selenium: {e}")
        return []

# Function to scrape URLs from sources
def scrape_urls(onion_url):
    urls = get_urls_with_requests(onion_url)
    if not urls:
        urls = get_urls_with_selenium(onion_url)
    return urls

# Function to store URLs in a database
def store_urls(urls):
    for url in urls:
        cur.execute("INSERT INTO urls (url) VALUES (%s)", (url,))
    con.commit()

# Recursive function to crawl links
def recursive_crawl(url, depth=0, depth_limit=3):
    if depth > depth_limit:
        return {}

    link_mapping = {}
    urls = scrape_urls(url)
    link_mapping[url] = urls

    for link in urls:
        link_mapping.update(recursive_crawl(link, depth+1, depth_limit))

    return link_mapping

# Function to store link mappings in a database
def store_mappings(mappings):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS mappings (
        id SERIAL PRIMARY KEY,
        url TEXT NOT NULL,
        links TEXT NOT NULL
    )
    ''')
    con.commit()

    for url, links in mappings.items():
        links_json = json.dumps(links)  # Convert list of links to JSON
        cur.execute("INSERT INTO mappings (url, links) VALUES (%s, %s)", (url, links_json))
    con.commit()

# Main program execution
def main():
    # User prompt for input URL and search keywords
    onion_url = input("Enter the starting .onion URL: ")
    search_keywords = input("Enter search keywords: ")

    # Create tables
    create_tables()

    # Scrape URLs from Torch search engine results
    search_urls = scrape_urls(f"http://xmh57jrzrnw6insl.onion/?q={search_keywords}")

    # For each URL in the search results
    for url in search_urls:
        # Scrape URLs from source
        urls = scrape_urls(url)

        # Store URLs in a database
        store_urls(urls)

        # Recursively crawl and map out link connections
        link_mapping = recursive_crawl(url)

        # Store link mappings in a database
        store_mappings(link_mapping)

    # Close database connection
    cur.close()
    con.close()

# Start the program
if __name__ == '__main__':
    main()
