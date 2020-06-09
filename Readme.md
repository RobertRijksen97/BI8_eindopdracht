
# Wat algemene info over de verschillende scripts 

Om alle data op te halen zijn deze bestanden gebruikt: 
(path erna toe: BI8_eindopdracht/scripts/pubmed/pubmed/spiders/)
  - GeneSelenium.py (de web crawler om van de site van hpo alle genen + synonymen te halen)
  - PubmedSpider.py (de web crawler die gebruikt is om per artikel alle genen + disease uit te halen)
  - pmc_result_second.txt (Hierin staan de gedownloade artikelen (PMC codes) 
  
Om alle letters van het alfabet door de GeneSelenium te halen: 
(path erna toe: BI8_eindopdracht/scripts/)
  - spider_run.py
  
De app.py is de gehele app. 

Volgende json bestanden zijn gebruikt:
  - pmc_twee.json (Hierin staan alle bestanden die door de PubmedSpider zijn gehaald 
  - gene.json (Hierin staat een subset van alle genen + synonymen die mbv de GeneSelenium spider is verkregen
