import scrapy
import json 
from urllib.parse import urljoin


class BrandsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        "https://mechanicalkeyboards.com/shop/index.php?l=product_list&c=110",
    ]

    def parse(self, response):
        categoryContainer = response.css(".category-list")
        brands = categoryContainer.xpath("//div[contains(@class, 'image')]/a/@href").extract()
        print("brands" + json.dumps(brands))
        for b in brands:
            url = urljoin(response.url, b)
            yield scrapy.Request(url, callback=self.parse_brand)

    def parse_brand(self, response):
        products = response.xpath("//div[contains(@class, 'product-name')]/a/@href").extract()
        print("products\n" + json.dumps(products))
        for p in products:
            url = urljoin(response.url + "&show=100", p)
            yield scrapy.Request(url, callback=self.parse_model)

    # def parse_product(self, response):
    #     models = response.xpath("//div[contains(@class, 'product-name')]/a/@href").extract()
    #     print("models\n" + json.dumps(models))
    #     for m in models:
    #         url = urljoin(response.url, m)
    #         yield scrapy.Request(url, callback=self.parse_model)

    def parse_model(self, response):
        css = ".v3_specs tr:nth-child({row}) td:nth-child(2)::text"
        findBasedOnText = "//*[contains(text(), '{text}')]/following::td/text()"
        # css = ".v3_specs tr:nth-child(1) td:nth-child(2)::text"
        # Target the specifications section for the juicy bits
        for info in response.css(".v3_specs"):
            # yield {
            #     "full_title": response.css(".header-detail .name::text").extract_first(),
            #     "brand": info.css(css.format(row=1)).extract_first(),
            #     "product_name": info.css(css.format(row=2)).extract_first(),
            #     "size": info.css(css.format(row=3)).extract_first(),
            #     "frame_color": info.css(css.format(row=7)).extract_first(),
            #     "primary_led_color": info.css(css.format(row=10)).extract_first(),
            #     "hotswappable": info.css(css.format(row=12)).extract_first(),
            #     "interfaces": info.css(css.format(row=18)).extract_first(),
            #     "windows_compatible": info.css(css.format(row=19)).extract_first(),
            #     "mac_compatible": info.css(css.format(row=20)).extract_first(),
            #     "dimensions": info.css(css.format(row=22)).extract_first(),
            #     "weight": info.css(css.format(row=23)).extract_first(),
            #     'price': info.css('#product_price::text').extract_first(),
            # }
            yield {
                "full_title": response.css(".header-detail .name::text").extract_first(),
                "features": response.xpath("//h3[contains(text(), 'Features')]/following::ul[@class='acc_features']/*/text()").getall(),
                "brand": info.css(css.format(row=1)).extract_first(),
                "product_name": info.css(css.format(row=2)).extract_first(),
                "size": info.xpath("//td[contains(text(), 'Size')]/following::td/text()").extract_first(),
                "frame_color": info.xpath(findBasedOnText.format(text="Frame Color")).extract_first(),
                "primary_led_color": info.xpath(findBasedOnText.format(text="Primary LED Color")).extract_first(),
                "hotswappable": info.xpath(findBasedOnText.format(text="Hotswap Sockets")).extract_first(),
                "interfaces": info.xpath(findBasedOnText.format(text="Interface(s)")).extract_first(),
                "windows_compatible": info.xpath(findBasedOnText.format(text="Windows Compatible")).extract_first(),
                "mac_compatible": info.xpath(findBasedOnText.format(text="Mac Compatible")).extract_first(),
                "linux_compatible": info.xpath(findBasedOnText.format(text="Linux Compatible")).extract_first(),
                "dimensions": info.xpath(findBasedOnText.format(text="Dimensions")).extract_first(),
                "weight": info.xpath(findBasedOnText.format(text="Weight")).extract_first(),
                'price': response.css('#product_price::text').extract_first(),
            }