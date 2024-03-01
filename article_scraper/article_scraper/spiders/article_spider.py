import scrapy
import pandas as pd
import os
from bs4 import BeautifulSoup

# Create the data directory if it doesn't exist
if not os.path.exists('../data'):
    os.makedirs('../data')
if not os.path.exists("../data/articles"):
    os.makedirs("../data/articles")


class ArticleSpider(scrapy.Spider):
    name = 'article_scraper'
    def start_requests(self):
        df = pd.read_excel('../task_definition_and_resources/Input.xlsx')
        for index, row in df.iterrows():
            url_id = row['URL_ID']
            url = row['URL']
            yield scrapy.Request(url=url, callback=self.parse, meta={'url_id': url_id})

    def parse(self, response):
        if response.status != 200:
            self.logger.warning(f"Failed to fetch {response.url} with status {response.status} with url_id {response.meta['url_id']}")
            return
        url_id = response.meta['url_id']
        title_html = response.css("div.td-full-screen-header-image-wrap > div.td-container.td-post-header > div.td-post-header-holder > div.td-parallax-header > header > h1")
        title = None
        title_css = "::text"
        if title_html.css("strong").extract_first() is not None:
            title_css = "strong::text"
        title = title_html.css(title_css).extract_first()
        if title is None:
            title = response.css("div > div.vc_column.tdi_120.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_title.tdi_122.tdb-single-title.td-pb-border-top.td_block_template_1 > div > h1::text").extract_first()
        raw_article_html = response.css("div.td-container > div > div.td-pb-span8.td-main-content > div > div.td-post-content.tagdiv-type").extract()
        if raw_article_html == []:
            raw_article_html = response.css("div > div.vc_column.tdi_120.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.td_block_wrap.tdb_single_content.tdi_130.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type > div").extract()
        soup = BeautifulSoup(" ".join(raw_article_html), 'lxml')
        text = soup.get_text(separator=" ", strip=True)

        if title is not None and text is not None:
            with open(f'../data/articles/{url_id}.txt', 'w') as f:
                f.write('\n'.join([title, text] ))
        else:
            self.logger.warning(f"Title or text is None for {url_id}")
            self.logger.warning(f"Title: {title}")
            self.logger.warning(f"Text: {text}")
            self.logger.warning(f"raw_article_html: {raw_article_html}")