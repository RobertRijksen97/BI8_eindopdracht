from scripts.pubmed.pubmed.spiders.pubmedSpider import PubmedSpider
from scrapy.crawler import CrawlerProcess


def main():
    process = CrawlerProcess()
    process.crawl(PubmedSpider, page='PMC6207735')
    process.start()


main()