# README



## Getting Started

```bash
# From adelie-scrape/mk, run:
source .venv/bin/activate
pip install 
```

## Running the crawlers

```bash
## run the crawler (requires Make)
make scrape 

## DELETE ALL THE OUTPUT DATA
make clean

## WIP: Create simple node scripts to clean and process the data
```

## Fine-tuning CSS

Using this view can help you hone in on the CSS you're looking for

```shell
# Initiate the interactive shell
scrapy shell https://mechanicalkeyboards.com/shop/index.php\?l\=product_list\&c\=110

# Start fiddling around with the path until a result is returned
response.xpath("//div[contains(@class, 'product-name')]/a/@href").extract()
```