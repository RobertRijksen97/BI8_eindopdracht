import string

import scrapy
from scrapy_splash import SplashRequest
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
# from selenium
from twisted.internet import defer

alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
url = 'https://hpo.jax.org/app/browse/search?q=a&navFilter=gene'
go = True

class gene_selenium(scrapy.Spider):
    name = 'Gene_finder_selenium'

    def __init__(self):
        super(gene_selenium, self).__init__()
        self.driver = webdriver.Firefox(executable_path=r'///home/robert/Documents/geckodriver/geckodriver-v0.26.0-linux64/geckodriver')

    def start_requests(self):
        # for letter in alph:
        letter = 'a'
        url = f'https://hpo.jax.org/app/browse/search?q={letter}&navFilter=gene'
        yield scrapy.Request(
            url=url,
            callback=self.parse_site)

    def parse_site(self, response):
        for item in self.getting_results(response):
            yield item
        # wait = WebDriverWait(self.driver, 5)
        # next_page = wait.until(
        #     expected_conditions.element_to_be_clickable((By.XPATH,
        #                                                  '//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-paginator/div/div/div[2]/button[2]/span/svg/path')))
        self.driver.get(response.url)
        w = WebDriverWait(self.driver, 40)
        # next_page = w.until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-paginator/div/div/div[2]/button[2]')))
        # next_page = self.driver.find_element_by_xpath('//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-paginator/div/div/div[2]/button[2]')
        btns = w.until(expected_conditions.presence_of_element_located((By.XPATH, '//button')))
        # btns = self.driver.find_elements_by_xpath('//button')
        print(btns)
        # for btn in btns:
        #     print(btn)
        #     txt = btn.text
        # next_page.click()
        for item in self.getting_results(response):
            yield item
        # except WebDriverException:
        #     print("LETTER DONE")

    def getting_results(self, response):
        for i in range(1, 2):
            self.driver.get(response.url)
            wait = WebDriverWait(self.driver, 40)
            print(i)
            element = wait.until(
                expected_conditions.element_to_be_clickable((By.XPATH,
                                                             f'//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-table/mat-row[{i}]/mat-cell[1]/a')))
            element.click()
            page_loading = wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div/app-gene/div/div/div[2]/div[2]/mat-card/mat-card-content/mat-list/mat-list-item/div/span')))
            gene = self.driver.find_element_by_class_name(
                "item-title").text
            print(gene)
            synonyms = self.driver.find_element_by_xpath(
                '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div/app-gene/div/div/div[2]/div[2]/mat-card/mat-card-content/mat-list/mat-list-item/div/span').text
            synonyms = synonyms[10:].split(',')
            synonyms.append(gene)
            print(synonyms)
            # self.driver.execute_script("window.history.go(-1)")
            self.driver.back()
            yield {gene: synonyms}



