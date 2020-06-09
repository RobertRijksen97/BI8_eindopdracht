# Naam: Robert Rijksen
# Datum: 2-6-2020
# Functie: Het ophalen van de diseases en genen uit een artikel van pubmed
# dmv een PMC code van het artikel

import scrapy


class PubmedSpider(scrapy.Spider):
    name = 'pubmed'

    def start_requests(self):
        """ De start_request functie haalt de url op uit het gedownloade pmc bestand.
        """
        with open('pmc_result_second.txt') as f:
            for line in f:
                self.page = line.strip('\n')
                yield scrapy.Request\
                    (url=f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids='
                         f'{self.page}', callback=self.parse)

    def parse(self, response):
        """ De functie parse haalt de scrapy.Request op en werkt met de response verder.
        :param response:
        """

        genes = []
        diseases = []
        for row in range(len(response.xpath('//passage/annotation/infon[@key="type"]/text()').getall())):
            if response.xpath('//passage/annotation/infon[@key="type"]/text()').getall()[row] == 'Gene':
                if response.xpath('//passage/annotation/text/text()').getall()[row] not in genes:
                    genes.append(response.xpath('//passage/annotation/text/text()').getall()[row])
            elif response.xpath('//passage/annotation/infon[@key="type"]/text()').getall()[row] == 'Disease':
                if response.xpath('//passage/annotation/text/text()').getall()[row].lower() not in diseases:
                    diseases.append(response.xpath('//passage/annotation/text/text()').getall()[row].lower())

        yield {"Article": [{"PMC": self.page, "genes": genes, "diseases": diseases}]}
