import scrapy

class PubmedSpider(scrapy.Spider):
    name = 'pubmed'

    def __init__(self, page=None, *args, **kwargs):
        super(PubmedSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids={page}']  # py36

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print(response.url)
        genes = []
        diseases = []

        for row in range(len(response.xpath('//passage/annotation/infon[@key="type"]/text()').getall())):
            if response.xpath('//passage/annotation/infon[@key="type"]/text()').getall()[row] == 'Gene':
                if response.xpath('//passage/annotation/text/text()').getall()[row] not in genes:
                    genes.append(response.xpath('//passage/annotation/text/text()').getall()[row])
            elif response.xpath('//passage/annotation/infon[@key="type"]/text()').getall()[row] == 'Disease':
                if response.xpath('//passage/annotation/text/text()').getall()[row].lower() not in diseases:
                    diseases.append(response.xpath('//passage/annotation/text/text()').getall()[row].lower())

        print('LIJST MET UNIEKE GENEN \n')
        print(genes)
        print('LIJST MET UNIEKE DISEASES \n')
        print(diseases)
        return genes, diseases
