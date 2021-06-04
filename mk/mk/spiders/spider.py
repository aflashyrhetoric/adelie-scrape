import scrapy
from pprint import pprint
import json
from urllib.parse import urljoin


class BrandsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        "https://mechanicalkeyboards.com/shop/index.php?l=product_list&c=110",
    ]

    def parse(self, response):
        categoryContainer = response.css(".category-list")
        brands = categoryContainer.xpath(
            "//div[contains(@class, 'image')]/a/@href"
        ).extract()
        print("brands" + json.dumps(brands))
        for b in brands:
            url = urljoin(response.url, b)
            yield scrapy.Request(url, callback=self.parse_brand)

    def parse_brand(self, response):
        products = response.xpath(
            "//div[contains(@class, 'product-name')]/a/@href"
        ).extract()
        print("products\n" + json.dumps(products))
        for p in products:
            url = urljoin(response.url + "&show=100", p)
            yield scrapy.Request(url, callback=self.parse_model)

    def parse_model(self, response):
        css = ".v3_specs tr:nth-child({row}) td:nth-child(2)::text"
        findBasedOnText = "//*[contains(text(), '{text}')]/following::td/text()"
        # imagePathPrefix = "https://mechanicalkeyboards.com/shop/{text}"
        # css = ".v3_specs tr:nth-child(1) td:nth-child(2)::text"
        # Target the specifications section for the juicy bits
        for info in response.css(".v3_specs"):
            # fmt: off
            frame_color = info.xpath(findBasedOnText.format(text="Frame Color")).extract_first()
            windows_compatible = info.xpath(findBasedOnText.format(text="Windows Compatible")).extract_first()
            mac_compatible = info.xpath(findBasedOnText.format(text="Mac Compatible")).extract_first()
            linux_compatible = info.xpath(findBasedOnText.format(text="Linux Compatible")).extract_first()
            size = info.xpath("//td[contains(text(), 'Size')]/following::td/text()").extract_first()
            interfaces = info.xpath(findBasedOnText.format(text="Interface(s)")).extract_first()
            available_switch_variants = response.css('.opt-table tr:first-child select option::text').getall()
            # fmt: on

            if frame_color is not None:
                # pprint(frame_color)
                frame_color = frame_color.lower()
            if windows_compatible is not None:
                # pprint(windows_compatible)
                windows_compatible = windows_compatible.lower()
                windows_compatible = windows_compatible == "yes"
            if mac_compatible is not None:
                mac_compatible = mac_compatible.lower()
                mac_compatible = mac_compatible == "yes"
            if linux_compatible is not None:
                linux_compatible = linux_compatible.lower()
                linux_compatible = linux_compatible == "yes"
            if size is not None:
                size = size.lower()
            if interfaces is not None:
                interfaces = interfaces.split(",")
            if available_switch_variants is not None:
                available_switch_variants = filter(lambda switch: ("Select One" not in switch), available_switch_variants)
                available_switch_variants = list(available_switch_variants)

            # fmt: off
            yield {
                "url": response.url,
                "sku": response.css(".product-id .id::text").extract_first(),
                "brand": info.css(css.format(row=1)).extract_first(),
                "product_name": info.css(css.format(row=2)).extract_first(),
                'price': response.css('#product_price::text').extract_first(),
                "product_description": response.css('.ldesc_fulldesc::text').extract_first(),
                "full_title": response.css(".header-detail .name::text").extract_first(),
                "features": response.xpath("//h3[contains(text(), 'Features')]/following::ul[@class='acc_features']/*/text()").getall(),
                "available_switch_variants": available_switch_variants,
                "size": size,
                "frame_color": frame_color,
                "primary_led_color": info.xpath(findBasedOnText.format(text="Primary LED Color")).extract_first(),
                "hotswappable": info.xpath(findBasedOnText.format(text="Hotswap Sockets")).extract_first(),
                "interfaces": interfaces,
                "windows_compatible": windows_compatible,
                "mac_compatible": mac_compatible,
                "linux_compatible": linux_compatible,
                "dimensions": info.xpath(findBasedOnText.format(text="Dimensions")).extract_first(),
                "weight": info.xpath(findBasedOnText.format(text="Weight")).extract_first(),
                "img_path": response.css('.product-info img::attr(src)').extract_first(),
            }
            # fmt: on
