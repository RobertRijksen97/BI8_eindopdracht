# Naam: Robert Rijksen
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

