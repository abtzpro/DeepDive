# DeepDive
A Darkweb forensic investigative tool in python

## Description (With help from AI)

This script is designed to perform web scraping and crawling on the darkweb, specifically targeting sites that end in .onion, which are accessible via the Tor network.

Here's a breakdown of its main functionality:

1. **Route traffic through Tor**: To access .onion sites, your network requests need to go through the Tor network. This script uses a library called `socks` to route all its network traffic through Tor.

2. **Establish connection to your database**: The script connects to a PostgreSQL database using the provided credentials and host information. This database is used to store the scraped data.

3. **Create necessary tables**: The script creates two tables in the database - 'urls' and 'mappings'. The 'urls' table stores the URLs found during the scraping process, and the 'mappings' table stores the link mappings (i.e., which links were found on each URL).

4. **Scrape URLs from sources**: The script sends a request to a given .onion URL and extracts all the 'a' tags with 'href' attribute that starts with 'http'. These are basically all the URLs found on the page.

5. **Store URLs in a database**: All scraped URLs are stored in the 'urls' table of the database.

6. **Recursive crawling**: For each URL found, the script visits it and looks for more URLs, repeating this process up to a specified depth limit.

7. **Store link mappings in a database**: For each URL visited, the script keeps track of all the links found on that page and stores this mapping in the 'mappings' table of the database.

8. **Use of Torch Tor search engine**: If you provide search keywords, the script will use these to search the Torch Tor search engine and scrape URLs from the search results, in addition to the initially provided .onion URL.

To use this script, the user would need to input a starting .onion URL and search keywords when prompted. The script then does all the scraping, storing, and mapping automatically. The results can be viewed in the connected PostgreSQL database.

Keep in mind, though, that web scraping and crawling, especially on the darkweb, may have ethical and legal considerations. Always ensure you are respecting privacy and following the law when using this script.

## Update v1.2 Features

- This script uses both requests and selenium to scrape URLs, and then stores these URLs in a PostgreSQL database. The script also creates a link mapping by recursively crawling through the URLs it finds, and these mappings are also stored in the database.
-
- The script uses a combination of Tor and Selenium to interact with .onion websites, often found on the dark web. It also handles exceptions and errors that might occur during the web scraping and database operations.
-
- The main() function drives the execution of the script by asking the user for an input URL and search keywords, performing the scraping, storing URLs, crawling links, and storing link mappings. The script then closes the database connection before exiting.

**As always, be sure to replace placeholders like “your_host”, “your_database”, “your_username”, and “your_password” with your actual PostgreSQL database details.**

## Features added soon in V2

Version 2

- This script will need to prompt the user to enter search keywords and then scrape URLs from the Torch search engine results for those keywords. It will then perform all the original scraping and crawling operations on each of those URLs and catch “control c” as a user exits prompting whether to export in CSV or HTML format, when a format is entered, the script will then output all of the database information as the chosen file type. 

-The script should include OSINT functionality incorporating known tools such as pipl, spider-foot, maltego POI search constraints, recondawg, email osint, proxy osint, proxy chains osint, and overall attempt to create a report of the identity behind the tor onion link. The osint logic should contain the ability to also fetch public results determined to be affiliated with the onion URL owner’s from the onion url owners local geographical area via clear net such as CCAP or clerk of district courts or otherwise.  

- The script should include mapping and infographic creation functionality to then map each user to their identity with a “logic map” section that explains how each connection was made to support legal proof of the onion URL user’s identity and how the conclusion was made. Essentially an infographic that depicts the steps taken to ascertain the identity. 

-The script should then include a social media pivot that allows a bot to navigate to the onion url owner’s social medias uncovered in the previous osint round. There extensive osint should be automated, performed and logged efficiently to the database in a table that contains the onion URLs with a section stating the URL owner’s identities turned up with osint for legal purposes to help catch cyber criminals using the darkweb as a means to market their wares and services. 

- The script should also check for communications between the threat actors logged within the database and log that to a new portion of the database specifically tailored to documenting threat actor communications regarding potentially abusive acts in order to help keep a watchful eye on threat actors and mitigate potential threat actors and their collaborative actions in the world of cyber. It could use a function that pivots between social medias and uses the pipl and similar tools to determine associates and then pivot to any information of the associates and affiliates that could potentially disclose the moniker or handle of the associates in turn using the same scraping function shown above to peruse any and all darkweb results using the torch search engine with the moniker or handle. 

- a feature to log network traffic coming and going where possible within thendatabase so as to document abusive threat actors/ buyers and their visits to these locations 

## Credits

- Developed by Adam Rivers
- Baseline Developed by AI
- Features and logic developed by Adam Rivers and Hello Security LLC

## Use case

DeepDive is being developed to assist cybersecurity researchers, federal investigators, private detectives and forensic investigators with darkweb investigations and fingerprinting threat actors therein. 


## Special Notes

DeepDive was designed dual purpose. Iniitally as a tool to help as described above as well as its secondary purpose, 

"to p*** off the attacker who revels in attacking one of my machines by hopefully making it much harder to obtain their tools. 

**That's right buddy, this one's for you**."
