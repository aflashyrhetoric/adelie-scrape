import scrapy
from urllib.parse import urljoin

class BrandsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://mechanicalkeyboards.com/shop/index.php?l=product_list&c=110',
    ]

    def parse(self, response):
        brands = response.xpath("//div[contains(@class, 'image')]/a/@href").extract()
        for b in brands:
            url = urljoin(response.url, b)
            yield scrapy.Request(url, callback=self.parse_brand)

    def parse_brand(self, response):
        products = response.xpath("//div[contains(@class, 'name')]/a/@href").extract()
        for p in products:
            url = urljoin(response.url, p)
            yield scrapy.Request(url, callback=self.parse_product)
            
    def parse_product(self, response):
        models = response.xpath("//div[contains(@class, 'product-name')]/a/@href").extract()
        for m in models:
            url = urljoin(response.url, m)
            yield scrapy.Request(url, callback=self.parse_model)



    def parse_model(self, response):
        css = ".v3_specs tr:nth-child({row}) td:nth-child(2)::text"
        # Target the specifications section for the juicy bits
        for info in response.css('.v3_specs'):
            yield {
                'model': info.css(css.format(row=1)).extract_first(),
                'product_name': info.css(css.format(row=2)).extract_first(),
                'layout': info.css(css.format(row=3)).extract_first(),
                'frame_color': info.css(css.format(row=7)).extract_first(),
                'lighting_type': info.css(css.format(row=10)).extract_first(),
                'hotswappable': info.css(css.format(row=12)).extract_first(),
                'dimensions': info.css(css.format(row=22)).extract_first(),
                'weight': info.css(css.format(row=23)).extract_first(),
                # 'product_image': info.css('div.ph-product-img-ctn a').xpath('@href').extract(),
                # 'sku': info.css('span.ph-pid').xpath('@prod-sku').extract_first(),
                # 'short_description': info.css('div.ph-product-summary::text').extract_first(),
                # 'price': info.css('h2.ph-product-price > span.price::text').extract_first(),
                # 'long_description': info.css('div#product_tab_1').extract_first(),
                # 'specs': info.css('div#product_tab_2').extract_first(),
            }