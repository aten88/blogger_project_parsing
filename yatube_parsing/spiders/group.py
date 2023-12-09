import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        all_grous = response.css('a[href^="/group/"]')
        for group_link in all_grous:
            yield response.follow(group_link, callback=self.parse_group)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        yield {
            'group_name': response.css('h2::text').get(),
            'description': response.css('p::text').get(),
            'posts_count': int(response.css('div.posts_count::text').re_first(
                r'Записей: (\d+)'
            ))
        }
