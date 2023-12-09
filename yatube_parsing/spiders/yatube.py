import scrapy


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        for message in response.css('div.card-body'):
            yield {
                'author': message.css('strong::text').get(),
                'text': ' '.join(message.css('p::text').getall()).strip(),
                'data': message.css('small::text').get()
            }
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
