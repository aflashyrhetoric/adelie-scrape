# README



## Getting Started

```bash
# From adelie-scrape/mk, run:
source .venv/bin/activate
pip install 
```

## Running the crawlers

```bash
## cd into `mk`
cd mk

## run the crawler (requires Make)
make scrape 

## DELETE ALL THE OUTPUT DATA
make clean

## Deploy the spiders to zyte (aka ScrapingHub)
# Make sure you're in adelie-scrape/mk with virtualenv activated first
make deploy 
```

## Fine-tuning CSS

Using this view can help you hone in on the CSS you're looking for

```shell
# Initiate the interactive shell
scrapy shell https://mechanicalkeyboards.com/shop/index.php\?l\=product_list\&c\=110
# for a specific product,
scrapy shell https://mechanicalkeyboards.com/shop/index.php\?l\=product_detail\&p\=5402

# Start fiddling around with the path until a result is returned
response.xpath("//div[contains(@class, 'product-name')]/a/@href").extract()
```