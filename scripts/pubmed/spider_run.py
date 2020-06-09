from scrapy.crawler import CrawlerProcess
from BI8_eindopdracht.scripts.pubmed.pubmed.spiders.GeneSelenium import GeneSelenium
# Deze import werkt lokaal zo, het kan zijn dat dit aangepast moet geven op github om de spider
# te importeren en te gebruiken

alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def main():
    count = 0
    for i in alph:
        # Via een forloop wordt elke letter in het alfabet door de spider gehaald. Zo wordt elk mogelijke
        count += 1
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': 'result' + str(count) + '.json'
        })

        process.crawl(GeneSelenium, letter=f'{i}')
        process.start()


main()
