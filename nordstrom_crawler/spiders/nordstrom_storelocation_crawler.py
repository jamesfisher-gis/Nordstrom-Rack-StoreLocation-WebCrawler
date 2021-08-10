# this focused web crawler is designed to crawl through the https://stores.nordstromrack.com website, extracting
# location and attribute data for all Nordstrom Rack stores. The crawler was designed with reproducibility in mind
# to periodically crawl the website for new or updated store listings.
# Author: James A. Fisher; jamesfisher.gis@gmail.com
import scrapy

class LocationCrawl(scrapy.Spider):
    name = 'StoreLocations'
    start_urls = ['https://stores.nordstromrack.com']

    # Advance from the root directory to level 1
    def parse(self, response):
       for link in response.css('a.Directory-listLink::attr(href)').getall():  # ['ca', 'us']
           yield response.follow(link, callback=self.parse_countries)
        # follow each of the country links and perform the parse_countries function.

    # Advance from level 1 (countries) to level 2 (states)
    def parse_countries(self, response):
        for link in response.css('a.Directory-listLink::attr(href)').getall():
            # ['us/ak/anchorage/680-east-northern-lights-boulevard', 'us/ny', 'us/pa', ...]
            # if only 1 store, the link will go directly to store page (ex. first element above)
            yield response.follow(link, callback=self.parse_states)
            #  follow each of the state/territory links and perform the parse states function

    # Advance from level 2 (states) to level 3 (Store Page, Location List, or City List)
    def parse_states(self, response):
        # determine if the webpage is a Store Page, LocationList, or CityList
        if response.xpath('//*[@id="main"]/div[3]/section/@class').get() == 'Directory Directory--ace CityList':
            # if a City List - ['us/ca/bakersfield, 'us/ca/burbank, ...]
            for link in response.css('a.Directory-listLink::attr(href)').getall():
                yield response.follow(link, callback=self.parse_city_list)

        elif response.xpath('//*[@id="main"]/div[3]/section/@class').get() == 'Directory Directory--ace LocationList':
            # if a Location List - ['us/ca/bakersfield/1-65--stockdale-hwy', 'us/ca/burbank/1601-n-victory-place', ...]
            for request in self.parse_location_list(response=response):
                yield request

        else:
            # store webpage - ('us/ak/anchorage/680-east-northern-lights-boulevard')
            for request in self.parse_store(response=response):
                yield request

    # Advance from level 3 (if page is a City List) to level 4 (Store Page or Location List)
    def parse_city_list(self, response):
        # if there are multiple locations in one city, page will be a Location List.
        if response.xpath('//*[@id="main"]/div[3]/section/@class').get() == 'Directory Directory--ace LocationList':
            # if a Location List - ['us/ca/bakersfield/1-65--stockdale-hwy', 'us/ca/burbank/1601-n-victory-place', ...]
            for request in self.parse_location_list(response=response):
                yield request
            # else the page will be a store page - parse and extract all data
        else:
            for request in self.parse_store(response=response):
                yield request

    # Advance from level 4 (if page is a Location List) to level 5 (Store Page) only if there is a live link.
    # Otherwise, extract all available data from the Location List
    def parse_location_list(self, response):
        for store in response.xpath('//*[@id="main"]/div[3]/section/div[2]/ul /li'):
            # if there is no link to a store page, pull all available data from the Location List page
            if store.css('a[data-ya-track="visitpage"]::attr(href)').get() == '../../':
                yield {
                    'name': store.css('span.LocationName-brand::text').get().strip(),
                    'address': store.css('span.c-address-street-1::text').get().strip(),
                    'city': store.css('span.c-address-city::text').get().strip(),
                    'region': store.css('abbr.c-address-state::text').get().strip(),
                    'postal_code': store.css('span.c-address-postal-code::text').get().strip(),
                    'country': store.css('abbr.c-address-country-name::text').get().strip(),
                    'phone': store.css('c-phone-number-span c-phone-main-number-span::text').get(),
                    'latitude': '',
                    'longitude': '',
                    'hours': '',
                }
            #  if there is a live link, follow to store page and extract all data
            else:
                yield response.follow(store.css('a[data-ya-track="visitpage"]::attr(href)').get()
                                      , callback=self.parse_store)

    # Extract all data from a Store Page
    def parse_store(self, response):
        store_info = response.css('div.NAP-info')  # element containing all of the store information
        yield {
            'name': store_info.css('span.LocationName-brand::text').get().strip(),
            'address': store_info.css('span.c-address-street-1::text').get().strip(),
            'city': store_info.css('span.c-address-city::text').get().strip(),
            'region': store_info.css('abbr.c-address-state::text').get().strip(),
            'postal_code': store_info.css('span.c-address-postal-code::text').get().strip(),
            'country': store_info.css('abbr.c-address-country-name::text').get().strip(),
            'phone': store_info.css('span.c-phone-number-span::text').get(),
            'latitude': store_info.css('meta[itemprop="latitude"]::attr(content)').get().strip(),
            'longitude': store_info.css('meta[itemprop="longitude"]::attr(content)').get().strip(),
            'hours': ' '.join(response.xpath('//*[@id="main"]/div[2]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div//text()').getall()[2:]),
        }
