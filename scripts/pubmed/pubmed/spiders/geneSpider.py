import string
import scrapy
from scrapy_splash import SplashRequest
import time


alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

url = 'https://hpo.jax.org/app/browse/search?q=a&navFilter=gene'


class geneSpider(scrapy.Spider):
    name = 'Gene_finder'

    loading_site = '''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(args.wait))
        return {
        html = splash:html(),
        }
    end 
    '''

    # def __init__(self):
    #     super(geneSpider, self).__init__()
    #     self.driver = webdriver.Firefox(executable_path=r'///home/robert/Documents/geckodriver/geckodriver-v0.26.0-linux64/geckodriver')

    def start_requests(self):
        # for letter in alph:
            # url = f'https://hpo.jax.org/app/browse/search?q={letter}&navFilter=gene'
        url = 'https://hpo.jax.org/app/browse/search?q=a&navFilter=gene'
        yield SplashRequest(
            url=url,
            endpoint='execute',
            args={'wait': 30, 'lua_source': self.loading_site},
            callback=self.parse_identity
        )

    def parse_site(self, response):
        print('SPLASH LOADIN')
        yield SplashRequest(
            url=response.url,
            endpoint='execute',
            args={'wait': 30, 'lua_source': self.loading_site},
            callback=self.parse_identity
        )

    def parse_identity(self, response):
        print('SPLASH DIDID IT')
        print(response.xpath('//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-table/mat-row[1]/mat-cell[1]/a').getall())

    def parse(self, response):
        # print(response.url)


        # all_results = self.driver.find_element_by_xpath('//*[@id="mat-option-8"]/span')
        # all_results.click()
        pos = 1


        for tab in response.xpath('//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-table'):
            if pos < 51:
                print(tab.xpath(f'/mat-row[{pos}]/mat-cell[1]/a').getall())
                pos += 1
        # print(response.xpath('//*[@id="mat-tab-content-5-2"]/div/div[1]/div'))
