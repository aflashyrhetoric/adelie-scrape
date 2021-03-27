.PHONY: scrape clean deploy

scrape:
	scrapy crawl products -o raw_data.json

clean:
	rm data.json

deploy:
	shub deploy 513726