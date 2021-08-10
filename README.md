# Nordstrom Rack Store Location Web Crawler
A focused web crawler aimed at https://stores.nordstromrack.com that will extract location and attribute data for all Nordstrom Rack stores

This focused web crawler is designed to crawl through the https://stores.nordstromrack.com website, extracting location and attribute data for all Nordstrom Rack stores. The crawler was developed with reproducibility in mind and can be periodically run to crawl the website for new or updated store listings.

The web crawler will extract the following data for all Nordstrom Rack stores:

Store name,  Address,  City,  State/Territory,  Postal code,  Country,  Phone number,  Latitude,  Longitude,  Hours of operation

### Website Structure

The goal of this web crawler is to navigate from the homepage, through the website structure, to each individual store and extract data about that store. The structure of https://stores.nordstromrack.com can be broken down into six(6) levels that aggregate stores at different geographic resolutions. The first three(3) of which are all stores on the homepage, countries (United States & Canada), and states/territories. 

![Nordstrom_websitestructuresmall](https://user-images.githubusercontent.com/85769594/128905045-14aa45d2-f81b-4eb4-a4a7-017a00dd832f.png)

The first three(3) levels are straitforward for a web crawler to navigate. However, it gets more complicated on level 3 where the crawler could arrive on any of three different types of web pages by following a state 'href' link. 

For example, if a state only has one(1) Nordstrom Rack store, the 'href' of that state will lead directly to the store page. If there are two(2) stores in a state, following the 'href' will lead to a list of the locations with some limited information about each. It is important to note that not every location has an associated store page. Where a location does not have a link to the detailed store page, we make due with the data available on the location list page. Lastly, if there are three(3) or more stores in a state the web crawler will land on a page showing a list of cities. Each city contains one(1) or more store locations with an 'href' that leads to either a store page or location list, respectively (level 4). 

From the description above, it is clear that the web crawler will need to look around as it explores the website to determine what page it has landed on and what to do next. 

To do this I implement a number of conditions that tell the the web crawler where it is, how to proceed to the next step, and when to extract data from the web page.

### Instructions

This project utilizes the Python Scrapy library (https://scrapy.org/) and can be run from the command terminal following the instructions below.


#### Step 1 – set directory to the Nordstrom_crawler file.
```
cd yourfilepath\nordstrom_crawler
```
#### Step 2 – create virtual environment
I strongly suggest working in a python 3 virtual environment when using Scrapy. The following will create a virtual environment named “venv”
```
py -m venv venv
```
Activate venv
```
.venv\Scripts\activate
```
#### Step 3 – install Scrapy
```
py  -m pip install scrapy
```
#### Step 4 – run the StoreLocations crawl
Enter the following command into the terminal to run the web crawler. The -o storelocations.csv command will write the extracted data to a .csv file named “storelocations” in the working directory.
```
scrapy crawl StoreLocations -o storelocations.csv
```
if you want to test modifications to the web crawler you may drop the -o command. Any errors will be returned in the terminal window.
```
scrapy crawl StoreLocations
```
#### Step 5 – compare the total number of records with the Nordstrom website
Compare to make sure the webcrawler is finding all store locations and is also not extracting duplicate records. One should also look at the data to confirm that there are no duplicates. 

Total number of Nordstrom Rack stores is given on the homepage - 353

Output from the python terminal:

![nordstromwebcrawll_ouput](https://user-images.githubusercontent.com/85769594/128913778-7970fee4-5961-4d23-89e3-1f40180afffa.png)

The web crawler has scraped 353 items from https://stores.nordstromrack.com, the same as the total number of stores.

Output location and attribute data file:

![Nordstrom_outputtable](https://user-images.githubusercontent.com/85769594/128913594-2be42f27-6b6d-4242-964e-4c207854c0be.png)

#### Step 6 – deactivate virtual environment
When you are finished, deactivate the python virtual environment
```
deactivate
```

Feel free to reach out with any questions or comments.

James A. Fisher

Email: jamesfisher.gis@gmail.com
