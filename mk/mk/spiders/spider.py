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
        # css = ".v3_specs tr:nth-child(1) td:nth-child(2)::text"
        # Target the specifications section for the juicy bits
        for info in response.css(".v3_specs"):
            yield {
                "full_title": response.css(".header-detail .name::text").extract_first(),
                "brand": info.css(css.format(row=1)).extract_first(),
                "product_name": info.css(css.format(row=2)).extract_first(),
                "size": info.css(css.format(row=3)).extract_first(),
                "frame_color": info.css(css.format(row=7)).extract_first(),
                "primary_led_color": info.css(css.format(row=10)).extract_first(),
                "hotswappable": info.css(css.format(row=12)).extract_first(),
                "interfaces": info.css(css.format(row=18)).extract_first(),
                "windows_compatible": info.css(css.format(row=19)).extract_first(),
                "mac_compatible": info.css(css.format(row=20)).extract_first(),
                "dimensions": info.css(css.format(row=22)).extract_first(),
                "weight": info.css(css.format(row=23)).extract_first(),
                'price': info.css('#product_price::text').extract_first(),
                # 'product_image': info.css('div.ph-product-img-ctn a').xpath('@href').extract(),
                # 'sku': info.css('span.ph-pid').xpath('@prod-sku').extract_first(),
                # 'short_description': info.css('div.ph-product-summary::text').extract_first(),
                # 'price': info.css('h2.ph-product-price > span.price::text').extract_first(),
                # 'long_description': info.css('div#product_tab_1').extract_first(),
                # 'specs': info.css('div#product_tab_2').extract_first(),
            }
