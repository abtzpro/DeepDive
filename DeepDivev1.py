import requests
from bs4 import BeautifulSoup
import psycopg2
import json
import socks
import socket

# Route traffic through Tor
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

# Function to scrape URLs from sources
def scrape_urls(onion_url):
    try:
        response = requests.get(onion_url)
    except requests.exceptions.RequestException as e:
        print(f"Could not make a request to the url: {onion_url}. Error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('http'):
            urls.append(link['href'])
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
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        outbound_links = []
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('http'):
                outbound_links.append(link['href'])

        link_mapping[url] = outbound_links

        for link in outbound_links:
            link_mapping.update(recursive_crawl(link, depth+1, depth_limit))

    except requests.exceptions.RequestException as e:
        print(f"Could not crawl url: {url}. Error: {e}")

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
