"""A module to deliver raw scraped web content."""

import requests
from lxml import html

class Spatula():
    """Scraped web content object for parsing"""

    def __init__(self, url):
        """Initialize attributes for scraper"""
        self.url = url
        self.tree = ''

    def scrape(self):
        """Download the content and load the contents"""
        page = requests.get(self.url)

        # Use `content` because `fromstring` expects bytes as input
        self.tree = html.fromstring(page.content)
        return self.tree