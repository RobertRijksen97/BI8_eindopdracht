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
        # wait = WebDriverWait(self.driver, 5)# Naam: Robert Rijksen
# Datum: 2-6-2020
# Functie: Het ophalen van alle genen + synonymen van hpo.

from abc import ABC

import scrapy

import time

import selenium
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
url = 'https://hpo.jax.org/app/browse/search?q=a&navFilter=gene'


class GeneSelenium(scrapy.Spider, ABC):
    name = 'Gene_finder_selenium'

    def __init__(self, letter=None, *args, **kwargs):
        super(GeneSelenium, self).__init__(*args, **kwargs)
        self.driver = webdriver.Firefox(executable_path=r'///home/robert/Documents/geckodriver/'
                                                        r'geckodriver-v0.26.0-linux64/geckodriver')
        self.start_urls = [f'https://hpo.jax.org/app/browse/search?q={letter}&navFilter=gene']

    def start_requests(self):
        for url_site in self.start_urls:
            yield scrapy.Request(
                url=url_site,
                callback=self.parse_site)

    def parse_site(self, response):
        for i in range(1, 51):
            self.driver.get(response.url)
            wait = WebDriverWait(self.driver, 50)
            element = wait.until(
                expected_conditions.element_to_be_clickable((By.XPATH,
                                                             f'//*[@id="mat-tab-content-0-2"]/div/div[1]/div/mat-table'
                                                             f'/mat-row[{i}]/mat-cell[1]/a')))
            element.click()

            time.sleep(5)
            gene = self.driver.find_element_by_class_name(
                "item-title").text

            try:
                synonyms = self.driver.find_element_by_xpath(
                    '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div'
                    '/app-gene/div/div/div[2]/div[2]/mat-card/mat-card-content/mat-list/mat-list-item/div/span').text
                synonyms = synonyms[10:].split(',')
                synonyms.append(gene)
                self.driver.back()
                yield {gene: synonyms}
            except selenium.common.exceptions.NoSuchElementException:
                synonyms = [gene]
                self.driver.back()
                yield {gene: synonyms}

        go = True
        count = 0
        while go:
            time.sleep(30)
            # Omdat de site super lang moet laden, en het met selenium webdriver.wait niet deed. Kon ik dit alleen maar
            # oplossen dmv een timesleep
            next_page = self.driver.find_element_by_xpath("//*[@aria-label='Next page']")
            count += 1
            next_page.click()
            for i in range(1, 51):
                # Een range van 50, omdat er 50 resultaten op de pagina staan.
                time.sleep(35)
                if i > 1:
                    # Hier wordt er doorgeklikt naar een nieuwe pagina.
                    next_page = self.driver.find_element_by_xpath(
                        "//*[@aria-label='Next page']")
                    for b in range(count):
                        # Omdat als je teruggaat naar de resultaten, je gelijk teruggaat naar de 1e pagina, moet er
                        # meerdere keren worden geklikt op de next page button. Bv. voor pagina 2 - 2x en
                        # voor pagina 3 - 3x etc.
                        time.sleep(2)
                        next_page.click()
                wait = WebDriverWait(self.driver, 5)
                element = wait.until(
                    expected_conditions.element_to_be_clickable((
                        By.XPATH, f'//div/div[1]/div/mat-table/mat-row[{i}]/mat-cell[1]/a')))
                element.click()
                time.sleep(5)
                # Hier wordt het gen opgehaald.
                gene = self.driver.find_element_by_class_name(
                    "item-title").text

                try:
                    # Hier worden de synonymen opgehaald, als deze aanwezig zijn.
                    synonyms = \
                        self.driver.find_element_by_xpath('/html/body/app-root/mat-sidenav-container/mat-sidenav-'
                                                          'content/div/app-gene/div/div/div[2]/div[2]/mat-card/'
                                                          'mat-card-content/mat-list/mat-list-item/div/span').text
                    synonyms = synonyms[10:].split(',')
                    synonyms.append(gene)
                    self.driver.back()
                    yield {gene: synonyms}
                except selenium.common.exceptions.NoSuchElementException:
                    synonyms = [gene]
                    self.driver.back()
                    yield {gene: synonyms}

        print("LETTER DONE")

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



